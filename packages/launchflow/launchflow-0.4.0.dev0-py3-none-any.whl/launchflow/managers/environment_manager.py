import asyncio
import os
import shutil
from typing import List, Optional, Union

import httpx
import yaml

from launchflow import exceptions
from launchflow.clients.environments_client import EnvironmentsAsyncClient
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.gcp_clients import get_storage_client, read_from_gcs, write_to_gcs
from launchflow.locks import GCSLock, LaunchFlowLock, LocalLock, Lock
from launchflow.managers.base import BaseManager
from launchflow.managers.resource_manager import ResourceManager
from launchflow.models.flow_state import Environment


def _load_local_environment(path: str, environment_name: str):
    base_env_path = os.path.join(path, environment_name)
    env_path = os.path.join(base_env_path, "flow.state")
    try:
        with open(env_path, "r") as f:
            raw_env = yaml.safe_load(f)
            env = Environment.model_validate(raw_env)
    except FileNotFoundError:
        raise exceptions.EnvironmentNotFound(environment_name)
    return env


async def _load_gcs_environment(bucket: str, prefix: str, environment_name: str):
    try:
        env_path = os.path.join(prefix, environment_name, "flow.state")
        raw_state = yaml.safe_load(await read_from_gcs(bucket, env_path))
        state = Environment.model_validate(raw_state)
        return state
    except exceptions.GCSObjectNotFound:
        raise exceptions.EnvironmentNotFound(environment_name)


async def _load_launchflow_environment(
    project_name: str,
    environment_name: str,
    launch_url: str,
    launch_api_key: Optional[str] = None,
):
    async with httpx.AsyncClient(timeout=60) as client:
        # TODO: take in the url and api key
        environments_client = EnvironmentsAsyncClient(
            client, launch_url, launch_api_key
        )
        try:
            state = await environments_client.get(project_name, environment_name)
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code == 404:
                raise exceptions.LaunchFlowEnvironmentNotFound(
                    project_name, environment_name
                )
            raise e

        return state


def _save_local_environment(environment: Environment, path: str, environment_name: str):
    env_path = os.path.join(path, environment_name)
    if not os.path.exists(env_path):
        os.makedirs(env_path)
    with open(os.path.join(env_path, "flow.state"), "w") as f:
        json_data = environment.to_dict()
        yaml.dump(json_data, f, sort_keys=False)


async def _save_gcs_environment(
    environment: Environment, bucket: str, prefix: str, environment_name: str
):
    env_path = os.path.join(prefix, environment_name, "flow.state")
    await write_to_gcs(
        bucket,
        env_path,
        yaml.dump(environment.to_dict(), sort_keys=False),
    )


async def _save_launchflow_environment(
    environment: Environment,
    project_name: str,
    environment_name: str,
    lock_id: str,
    launch_url: str,
    launch_api_key: Optional[str],
):
    async with httpx.AsyncClient() as client:
        env_client = EnvironmentsAsyncClient(client, launch_url, launch_api_key)
        await env_client.create(
            project_name=project_name,
            env_name=environment_name,
            environment=environment,
            lock_id=lock_id,
        )


class EnvironmentManager(BaseManager):

    def __init__(
        self,
        project_name: str,
        environment_name: str,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    ) -> None:
        super().__init__(backend)
        self.project_name = project_name
        self.environment_name = environment_name

    async def load_environment(self) -> Environment:
        if isinstance(self.backend, LocalBackend):
            return _load_local_environment(self.backend.path, self.environment_name)
        elif isinstance(self.backend, LaunchFlowBackend):
            return await _load_launchflow_environment(
                self.project_name,
                self.environment_name,
                self.backend.launchflow_url,
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            return await _load_gcs_environment(
                self.backend.bucket, self.backend.prefix, self.environment_name
            )

    async def save_environment(self, environment: Environment, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            _save_local_environment(
                environment, self.backend.path, self.environment_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            await _save_launchflow_environment(
                environment,
                self.project_name,
                self.environment_name,
                lock_id,
                self.backend.launchflow_url,
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            await _save_gcs_environment(
                environment,
                self.backend.bucket,
                self.backend.prefix,
                self.environment_name,
            )
        else:
            raise NotImplementedError("Only local backend is supported")

    def lock_environment(self, operation: str) -> Lock:
        if isinstance(self.backend, LocalBackend):
            env_path = os.path.join(self.backend.path, self.environment_name)
            return LocalLock(env_path, operation)
        elif isinstance(self.backend, GCSBackend):
            return GCSLock(
                self.backend.bucket,
                self.backend.prefix,
                self.environment_name,
                operation,
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return LaunchFlowLock(
                project=self.project_name,
                entity_path=f"environments/{self.environment_name}",
                operation=operation,
                launch_url=self.backend.launchflow_url,
                launchflow_api_key=self.backend.launchflow_api_key,
            )
        else:
            raise NotImplementedError("Only local backend is supported")

    async def delete_environment(self, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            shutil.rmtree(os.path.join(self.backend.path, self.environment_name))
        elif isinstance(self.backend, GCSBackend):

            def delete_blobs():
                client = get_storage_client()
                blobs = client.list_blobs(
                    bucket_or_name=self.backend.bucket,
                    prefix=os.path.join(self.backend.prefix, self.environment_name),
                )
                for blob in blobs:
                    blob.delete()

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, delete_blobs)
        elif isinstance(self.backend, LaunchFlowBackend):
            async with httpx.AsyncClient() as client:
                env_client = EnvironmentsAsyncClient(
                    client, self.backend.launchflow_url, self.backend.launchflow_api_key
                )
                await env_client.delete(
                    project_name=self.project_name,
                    env_name=self.environment_name,
                    lock_id=lock_id,
                )

    # TODO Revisit whether this method should return managers or resources
    # TODO Test this
    async def list_resource_managers(self) -> List[ResourceManager]:
        if isinstance(self.backend, LocalBackend):
            resource_dir = os.path.join(self.backend.path, self.environment_name, "resources")
            resource_names = os.listdir(resource_dir)
        else:
            raise NotImplementedError

        resource_managers = []
        for name in resource_names:
            resource_managers.append(ResourceManager(
                project_name=self.project_name,
                environment_name=self.environment_name,
                resource_name=name,
                backend=self.backend,
            ))

        return resource_managers
