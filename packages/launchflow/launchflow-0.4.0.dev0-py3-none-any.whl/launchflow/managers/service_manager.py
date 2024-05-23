import os
from typing import Union

import httpx
import yaml

from launchflow import exceptions
from launchflow.clients.services_client import ServicesAsyncClient
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.gcp_clients import read_from_gcs, write_to_gcs
from launchflow.managers.base import BaseManager
from launchflow.models.flow_state import Service

# TODO: need to add tests to this file once it is all working


def _load_local_service(path: str, name: str, env_name: str):
    base_service_path = os.path.join(path, env_name, "services", name)
    service_path = os.path.join(base_service_path, "flow.state")
    with open(service_path, "r") as f:
        raw_service = yaml.safe_load(f)
        service = Service.model_validate(raw_service)
    return service


async def _load_gcs_service(
    bucket: str, prefix: str, environment_name: str, service_name: str
):
    # TODO: throw a not found error if we can't find the environment
    env_path = os.path.join(
        prefix, environment_name, "services", service_name, "flow.state"
    )
    try:
        raw_state = yaml.safe_load(await read_from_gcs(bucket, env_path))
        state = Service.model_validate(raw_state)
    except exceptions.GCSObjectNotFound:
        raise exceptions.ServiceNotFound(service_name)
    return state


async def _load_launchflow_service(
    project_name: str, environment_name: str, service_name: str
) -> Service:
    async with httpx.AsyncClient(timeout=60) as client:
        # TODO: take in the url and api key
        services_client = ServicesAsyncClient(client)
        try:
            state = await services_client.get(
                project_name, environment_name, service_name
            )
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code == 404:
                raise exceptions.LaunchFlowServiceNotFound(
                    project_name, environment_name, service_name
                )
            raise e

        return state


def _save_local_service(
    service: Service, path: str, environment_name: str, service_name: str
):
    service_path = os.path.join(path, environment_name, "services", service_name)
    service_file = os.path.join(service_path, "flow.state")
    if not os.path.exists(service_path):
        os.makedirs(service_path)
    with open(service_file, "w") as f:
        json_data = service.to_dict()
        yaml.dump(json_data, f, sort_keys=False)


async def _save_gcs_service(
    service: Service,
    bucket: str,
    prefix: str,
    environment_name: str,
    service_name: str,
):
    service_path = os.path.join(
        prefix, environment_name, "services", service_name, "flow.state"
    )
    await write_to_gcs(
        bucket,
        service_path,
        yaml.dump(service.to_dict(), sort_keys=False),
    )


async def _save_launchflow_service(
    service: Service,
    project_name: str,
    environment_name: str,
    service_name: str,
    lock_id: str,
):
    raise NotImplementedError("Saving services to LaunchFlow is not supported")


class ServiceManager(BaseManager):

    def __init__(
        self,
        project_name: str,
        environment_name: str,
        service_name: str,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    ) -> None:
        super().__init__(backend)
        self.project_name = project_name
        self.environment_name = environment_name
        self.service_name = service_name

    async def load_service(self) -> Service:
        if isinstance(self.backend, LocalBackend):
            return _load_local_service(
                self.backend.path, self.service_name, self.environment_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            return await _load_launchflow_service(
                self.project_name, self.environment_name, self.service_name
            )
        elif isinstance(self.backend, GCSBackend):
            return await _load_gcs_service(
                self.backend.bucket,
                self.backend.prefix,
                self.environment_name,
                self.service_name,
            )

    async def save_service(self, service: Service, lock_id: str):
        if isinstance(self.backend, LocalBackend):
            _save_local_service(
                service, self.backend.path, self.environment_name, self.service_name
            )
        elif isinstance(self.backend, LaunchFlowBackend):
            await _save_launchflow_service(
                service,
                self.project_name,
                self.environment_name,
                self.service_name,
                lock_id,
            )
        elif isinstance(self.backend, GCSBackend):
            await _save_gcs_service(
                service,
                self.backend.bucket,
                self.backend.prefix,
                self.environment_name,
                self.service_name,
            )
