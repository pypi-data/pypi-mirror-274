import os
import shutil
from typing import Union

import httpx
import yaml

from launchflow import exceptions
from launchflow.clients.resources_client import ResourcesAsyncClient
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.gcp_clients import read_from_gcs, write_to_gcs
from launchflow.locks import GCSLock, LaunchFlowLock, LocalLock, Lock
from launchflow.managers.base import BaseManager
from launchflow.models.flow_state import Resource

# TODO: need to add tests to this file once it is all working


def _load_local_resource(path: str, name: str, env_name: str):
    base_resource_path = os.path.join(path, env_name, "resources", name)
    resource_path = os.path.join(base_resource_path, "flow.state")
    with open(resource_path, "r") as f:
        raw_resource = yaml.safe_load(f)
        resource = Resource.model_validate(raw_resource)
    return resource


async def _load_gcs_resource(
    bucket: str, prefix: str, environment_name: str, resource_name: str
):
    # TODO: throw a not found error if we can't find the environment
    env_path = os.path.join(
        prefix, environment_name, "resources", resource_name, "flow.state"
    )
    try:
        raw_state = yaml.safe_load(await read_from_gcs(bucket, env_path))
        state = Resource.model_validate(raw_state)
    except exceptions.GCSObjectNotFound:
        raise exceptions.ResourceNotFound(resource_name)
    return state


async def _load_launchflow_resource(
    project_name: str, environment_name: str, resource_name: str
) -> Resource:
    async with httpx.AsyncClient(timeout=60) as client:
        # TODO: take in the url and api key
        resources_client = ResourcesAsyncClient(client)
        try:
            state = await resources_client.get(
                project_name, environment_name, resource_name
            )
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code == 404:
                raise exceptions.LaunchFlowResourceNotFound(
                    project_name, environment_name, resource_name
                )
            raise e

        return state


def _save_local_resource(
    resource: Resource, path: str, environment_name: str, resource_name: str
):
    resource_path = os.path.join(path, environment_name, "resources", resource_name)
    resource_file = os.path.join(resource_path, "flow.state")
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
    with open(resource_file, "w") as f:
        json_data = resource.to_dict()
        yaml.dump(json_data, f, sort_keys=False)


def _delete_local_resource(
    path: str, environment_name: str, resource_name: str
):
    resource_path = os.path.join(path, environment_name, "resources", resource_name)
    shutil.rmtree(resource_path)


async def _save_gcs_resource(
    resource: Resource,
    bucket: str,
    prefix: str,
    environment_name: str,
    resource_name: str,
):
    resource_path = os.path.join(
        prefix, environment_name, "resources", resource_name, "flow.state"
    )
    await write_to_gcs(
        bucket,
        resource_path,
        yaml.dump(resource.to_dict(), sort_keys=False),
    )


async def _save_launchflow_resource(
    resource: Resource,
    project_name: str,
    environment_name: str,
    resource_name: str,
    lock_id: str,
):
    raise NotImplementedError("Saving resources to LaunchFlow is not supported")


class ResourceManager(BaseManager):

    def __init__(
        self,
        project_name: str,
        environment_name: str,
        resource_name: str,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    ) -> None:
        super().__init__(backend)
        self.project_name = project_name
        self.environment_name = environment_name
        self.resource_name = resource_name

    async def load_resource(self) -> Resource:
        if isinstance(self.backend, LocalBackend):
            return _load_local_resource(
                self.backend.path, self.resource_name, self.environment_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return await _load_launchflow_resource(
                self.project_name, self.environment_name, self.resource_name
            )
        elif isinstance(self.backend, GCSBackend):
            return await _load_gcs_resource(
                self.backend.bucket,
                self.backend.prefix,
                self.environment_name,
                self.resource_name,
            )

    async def save_resource(self, resource: Resource, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            _save_local_resource(
                resource, self.backend.path, self.environment_name, self.resource_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            await _save_launchflow_resource(
                resource,
                self.project_name,
                self.environment_name,
                self.resource_name,
                lock_id,
            )
        elif isinstance(self.backend, GCSBackend):
            await _save_gcs_resource(
                resource,
                self.backend.bucket,
                self.backend.prefix,
                self.environment_name,
                self.resource_name,
            )

    async def delete_resource(self, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            _delete_local_resource(
                self.backend.path, self.environment_name, self.resource_name,
            )
        else:
            raise NotImplementedError

    def lock_resource(self, operation: str) -> Lock:
        if isinstance(self.backend, LocalBackend):
            env_path = os.path.join(self.backend.path, self.environment_name, "resources", self.resource_name)
            return LocalLock(env_path, operation)
        elif isinstance(self.backend, GCSBackend):
            return GCSLock(
                self.backend.bucket,
                self.backend.prefix,
                f"{self.environment_name}/{self.resource_name}",
                operation,
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return LaunchFlowLock(
                project=self.project_name,
                entity_path=f"environments/{self.environment_name}/resources/{self.resource_name}",
                operation=operation,
                launch_url=self.backend.launchflow_url,
                launchflow_api_key=self.backend.launchflow_api_key,
            )
        else:
            raise NotImplementedError("Only local backend is supported")
