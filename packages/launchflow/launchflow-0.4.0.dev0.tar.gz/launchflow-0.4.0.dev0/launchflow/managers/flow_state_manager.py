import asyncio
import os
from typing import Dict, Union

import httpx
import yaml

from launchflow import exceptions
from launchflow.clients.environments_client import EnvironmentsAsyncClient
from launchflow.clients.projects_client import ProjectsAsyncClient
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.gcp_clients import get_storage_client, read_from_gcs, write_to_gcs
from launchflow.managers.base import BaseManager
from launchflow.models.flow_state import Environment, FlowState


def _save_local_flow_state(flow_state: FlowState, path: str):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
    flow_path = os.path.join(abs_path, "flow.state")
    with open(flow_path, "w") as f:
        json_data = flow_state.to_dict()
        yaml.dump(json_data, f, sort_keys=False)


async def _save_gcs_flow_state(flow_state: FlowState, bucket: str, prefix: str):
    base_path = os.path.join(prefix, "flow.state")
    await write_to_gcs(
        bucket,
        base_path,
        yaml.dump(flow_state.to_dict(), sort_keys=False),
    )


async def _load_flow_state_from_gcs(backend: GCSBackend):
    flow_path = os.path.join(backend.prefix, "flow.state")
    try:
        raw_state = yaml.safe_load(await read_from_gcs(backend.bucket, flow_path))
        state = FlowState.model_validate(raw_state)
        return state
    except exceptions.GCSObjectNotFound:
        raise exceptions.FlowStateNotFound()


async def _load_flow_state_from_launchflow(
    project_name: str, launch_flow_url: str, launch_flow_api_key: str
):
    async with httpx.AsyncClient(timeout=60) as client:
        projects_client = ProjectsAsyncClient(
            client, launch_flow_url, launch_flow_api_key
        )
        try:
            state = await projects_client.get(project_name)
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code == 404:
                raise exceptions.LaunchFlowProjectNotFound(project_name)
            raise e

        return state


def _load_flow_state_from_local(backend: LocalBackend):
    flow_path = os.path.join(os.path.abspath(backend.path), "flow.state")
    try:
        with open(flow_path, "r") as f:
            raw_flow_state = yaml.safe_load(f)
            flow_state = FlowState.model_validate(raw_flow_state)
    except FileNotFoundError:
        raise exceptions.FlowStateNotFound()
    return flow_state


class FlowStateManager(BaseManager):

    def __init__(
        self,
        project_name: str,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    ) -> None:
        super().__init__(
            backend=backend,
        )
        self.project_name: str = project_name

    async def load_flow_state(self) -> FlowState:
        if isinstance(self.backend, LocalBackend):
            return _load_flow_state_from_local(self.backend)
        elif isinstance(self.backend, LaunchFlowBackend):
            return await _load_flow_state_from_launchflow(
                self.project_name,
                self.backend.launchflow_url,
                self.backend.launchflow_api_key,
            )
        elif isinstance(self.backend, GCSBackend):
            return await _load_flow_state_from_gcs(self.backend)

    async def save_flow_state(self, flow_state: FlowState) -> None:
        if isinstance(self.backend, LocalBackend):
            _save_local_flow_state(flow_state, self.backend.path)
        elif isinstance(self.backend, GCSBackend):
            await _save_gcs_flow_state(
                flow_state, self.backend.bucket, self.backend.prefix
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            # NOTE: inpractice this will never be called because this is only used for tests
            raise ValueError(
                "LaunchFlow flow state should be saved using `launchflow projects create`"
            )
        else:
            raise NotImplementedError("Only local backend is supported")

    async def list_environments(self) -> Dict[str, Environment]:
        if isinstance(self.backend, LocalBackend):
            # Load the environments
            envs = {}
            for dir in os.scandir(self.backend.path):
                if dir.is_dir():
                    if os.path.exists(os.path.join(dir.path, "flow.state")):
                        env_name = os.path.basename(dir.path)
                        env_path = os.path.join(dir.path, "flow.state")
                        with open(env_path, "r") as f:
                            raw_env = yaml.safe_load(f)
                            env = Environment.model_validate(raw_env)
                            envs[env_name] = env
            return envs
        elif isinstance(self.backend, LaunchFlowBackend):
            async with httpx.AsyncClient(timeout=60) as client:
                env_client = EnvironmentsAsyncClient(
                    client, self.backend.launchflow_url, self.backend.launchflow_api_key
                )
                try:
                    return await env_client.list(self.project_name)
                except exceptions.LaunchFlowRequestFailure as e:
                    if e.status_code == 404:
                        raise exceptions.LaunchFlowProjectNotFound(self.project_name)
                    raise e
        elif isinstance(self.backend, GCSBackend):
            gcs_client = get_storage_client()
            bucket = gcs_client.bucket(self.backend.bucket)
            blobs = bucket.list_blobs(prefix=self.backend.prefix)
            envs = {}

            def read_blobs():
                for blob in blobs:
                    relative_path = blob.name.replace(f"{self.backend.prefix}/", "")
                    split_path = relative_path.split("/")
                    if relative_path.endswith("flow.state") and len(split_path) == 2:
                        env_name = blob.name.split("/")[-2]
                        raw_env = yaml.safe_load(blob.download_as_string())
                        env = Environment.model_validate(raw_env)
                        envs[env_name] = env
                return envs

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, read_blobs)
