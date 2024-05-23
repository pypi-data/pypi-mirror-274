import logging
import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import fsspec
import httpx
import yaml

import launchflow
from launchflow import exceptions
from launchflow.cache import cache
from launchflow.cli.utils import tar_source_in_memory
from launchflow.clients.client import LaunchFlowAsyncClient
from launchflow.clients.environments_client import (
    EnvironmentsAsyncClient,
    EnvironmentsSyncClient,
)
from launchflow.clients.resources_client import (
    ResourcesAsyncClient,
    ResourcesSyncClient,
)
from launchflow.clients.services_client import ServicesAsyncClient
from launchflow.config import config
from launchflow.operations import (
    AsyncEntityOp,
    AsyncResourceNoOp,
    AsyncResourcePendingOp,
)


def maybe_clear_resource_cache(
    project_name: str,
    environment_name: str,
    product_name: str,
    resource_name: str,
):
    try:
        cache.delete_resource_connection_info(
            project_name, environment_name, product_name, resource_name
        )
        cache.delete_resource_connection_bucket_path(
            project_name, environment_name, product_name, resource_name
        )
    except Exception as e:
        logging.warning(f"Failed to delete resource connection info from cache: {e}")
        pass


@dataclass
class _ResourceURI:
    project_name: str
    environment_name: str
    product_name: str
    resource_name: str

    def __repr__(self) -> str:
        return f"{self.project_name}/{self.environment_name}/{self.resource_name}"

    @classmethod
    def create(
        cls,
        project_name: Optional[str],
        environment_name: Optional[str],
        product_name: str,
        resource_name: str,
    ) -> "_ResourceURI":
        project_name = project_name or launchflow.project
        environment_name = environment_name or launchflow.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        return _ResourceURI(
            project_name=project_name,
            environment_name=environment_name,
            product_name=product_name,
            resource_name=resource_name,
        )


# Step 1: Check if the connection info should be fetched from a mounted volume
def _load_connection_info_from_mounted_volume(resource_uri: _ResourceURI):
    if config.env.connection_path is not None:
        local_resource_path = os.path.join(
            config.env.connection_path, resource_uri.resource_name, "latest"
        )
        if not os.path.exists(local_resource_path):
            logging.warning(
                f"Connection info for resource '{resource_uri}' not found on disk."
            )
        else:
            with open(local_resource_path) as f:
                return yaml.load(f, Loader=yaml.FullLoader)


# Step 2: Check the cache for connection info, otherwise fetch from remote
def _load_connection_info_from_cache(resource_uri: _ResourceURI):
    resource_connection_info = cache.get_resource_connection_info(
        resource_uri.project_name,
        resource_uri.environment_name,
        resource_uri.product_name,
        resource_uri.resource_name,
    )
    if resource_connection_info is not None:
        logging.debug(f"Using cached resource connection info for {resource_uri}")
        return resource_connection_info


# Step 3a: Load connection bucket from environment variable
def _get_connection_bucket_path_from_local(resource_uri: _ResourceURI):
    if config.env.connection_bucket is not None:
        # If the bucket env var is set, we use it to build the connection path
        connection_bucket_path = f"{config.env.connection_bucket}/resources/{resource_uri.resource_name}.yaml"
        logging.debug(
            "Using connection bucket path built from environment variable for {resource_uri}"
        )
    else:
        # If the bucket env var is not set, we check the cache or fetch from remote
        connection_bucket_path = cache.get_resource_connection_bucket_path(
            resource_uri.project_name,
            resource_uri.environment_name,
            resource_uri.product_name,
            resource_uri.resource_name,
        )
    return connection_bucket_path


async def _get_connection_bucket_from_remote_async(
    client: ResourcesAsyncClient, resource_uri: _ResourceURI
):
    resource = await client.get(
        project_name=resource_uri.project_name,
        environment_name=resource_uri.environment_name,
        resource_name=resource_uri.resource_name,
        product_name_to_validate=resource_uri.product_name,
    )
    return resource.connection_bucket_path


def _get_connection_bucket_from_remote_sync(
    client: ResourcesSyncClient, resource_uri: _ResourceURI
):
    resource = client.get(
        project_name=resource_uri.project_name,
        environment_name=resource_uri.environment_name,
        resource_name=resource_uri.resource_name,
        product_name_to_validate=resource_uri.product_name,
    )
    return resource.connection_bucket_path


def _load_connection_info_from_remote_bucket(
    connection_bucket_path: str, resource_name: str
):
    try:
        # TODO: Support async file reading (fsspec supports it)
        with fsspec.open(connection_bucket_path, mode="r") as file:
            resource_connection_info = yaml.safe_load(file.read())
    except FileNotFoundError:
        raise exceptions.ConnectionInfoNotFound(resource_name)
    except PermissionError:
        raise exceptions.PermissionCannotReadConnectionInfo(
            resource_name=resource_name, connection_path=connection_bucket_path
        )
    except Exception as e:
        if connection_bucket_path.startswith("gs://"):
            bucket_name = connection_bucket_path.removeprefix("gs://").split("/")[0]
            bucket_url = (
                f"https://console.cloud.google.com/storage/browser/{bucket_name}"
            )
        else:
            bucket_name = connection_bucket_path.removeprefix("s3://").split("/")[0]
            bucket_url = f"https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}"
        raise exceptions.ForbiddenConnectionInfo(bucket_url) from e

    return resource_connection_info


def _load_gcp_service_account_email_from_cache(
    project_name: str, environment_name: str
):
    gcp_service_account_email = cache.get_gcp_service_account_email(
        project_name, environment_name
    )
    if gcp_service_account_email is not None:
        logging.debug(
            f"Using cached GCP service account email for {project_name}/{environment_name}"
        )
        return gcp_service_account_email


@dataclass
class LaunchFlowContext:
    api_key: Optional[str] = None
    _resource_async_client: Optional[ResourcesAsyncClient] = None
    _resource_sync_client: Optional[ResourcesSyncClient] = None
    _environment_async_client: Optional[EnvironmentsAsyncClient] = None
    _environment_sync_client: Optional[EnvironmentsSyncClient] = None
    _service_async_client: Optional[ServicesAsyncClient] = None
    _lf_client: Optional[LaunchFlowAsyncClient] = None

    @property
    def lf_client(self):
        if self._lf_client is None:
            self._lf_client = LaunchFlowAsyncClient(self.api_key)
        return self._lf_client

    @property
    def resource_async_client(self):
        if self._resource_async_client is None:
            self._resource_async_client = ResourcesAsyncClient(
                httpx.AsyncClient(timeout=60), self.api_key
            )
        return self._resource_async_client

    @property
    def resource_sync_client(self):
        if self._resource_sync_client is None:
            self._resource_sync_client = ResourcesSyncClient(
                httpx.Client(timeout=60), self.api_key
            )
        return self._resource_sync_client

    @property
    def environment_async_client(self):
        if self._environment_async_client is None:
            self._environment_async_client = EnvironmentsAsyncClient(
                httpx.AsyncClient(timeout=60), self.api_key
            )
        return self._environment_async_client

    @property
    def environment_sync_client(self):
        if self._environment_sync_client is None:
            self._environment_sync_client = EnvironmentsSyncClient(
                httpx.Client(timeout=60), self.api_key
            )
        return self._environment_sync_client

    @property
    def service_async_client(self):
        if self._service_async_client is None:
            self._service_async_client = ServicesAsyncClient(
                httpx.AsyncClient(timeout=60), self.api_key
            )
        return self._service_async_client

    def get_resource_connection_info_sync(
        self,
        product_name: str,
        resource_name: str,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
    ) -> Dict:
        resource_uri = _ResourceURI.create(
            project_name, environment_name, product_name, resource_name
        )
        # Load connection info from mounted volume
        resource_connection_info = _load_connection_info_from_mounted_volume(
            resource_uri
        )
        if resource_connection_info:
            return resource_connection_info

        # Load connection info from cache
        resource_connection_info = _load_connection_info_from_cache(resource_uri)
        if resource_connection_info:
            return resource_connection_info

        # Load connection info from remote bucket
        connection_bucket_path = _get_connection_bucket_path_from_local(resource_uri)
        if connection_bucket_path is None:
            connection_bucket_path = _get_connection_bucket_from_remote_sync(
                self.resource_sync_client, resource_uri
            )

        resource_connection_info = _load_connection_info_from_remote_bucket(
            connection_bucket_path, resource_uri.resource_name
        )
        cache.set_resource_connection_info(
            resource_uri.project_name,
            resource_uri.environment_name,
            resource_uri.product_name,
            resource_uri.resource_name,
            resource_connection_info,
        )
        return resource_connection_info

    def create_resource_operation_sync(
        self,
        product_name: str,
        resource_name: str,
        create_args: Dict,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        replace: bool = False,
    ):
        raise NotImplementedError(
            "create_resource_operation_sync is not implemented yet. Use create_resource_operation_async instead."
        )

    async def get_resource_connection_info_async(
        self,
        product_name: str,
        resource_name: str,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
    ) -> Dict:
        resource_uri = _ResourceURI.create(
            project_name, environment_name, product_name, resource_name
        )
        # Load connection info from mounted volume
        resource_connection_info = _load_connection_info_from_mounted_volume(
            resource_uri
        )
        if resource_connection_info:
            return resource_connection_info

        # Load connection info from cache
        resource_connection_info = _load_connection_info_from_cache(resource_uri)
        if resource_connection_info:
            return resource_connection_info

        # Load connection info from remote bucket
        connection_bucket_path = _get_connection_bucket_path_from_local(resource_uri)
        if connection_bucket_path is None:
            connection_bucket_path = await _get_connection_bucket_from_remote_async(
                self.resource_async_client, resource_uri
            )

        resource_connection_info = _load_connection_info_from_remote_bucket(
            connection_bucket_path, resource_uri.resource_name
        )
        cache.set_resource_connection_info(
            resource_uri.project_name,
            resource_uri.environment_name,
            resource_uri.product_name,
            resource_uri.resource_name,
            resource_connection_info,
        )
        return resource_connection_info

    async def create_resource_operation_async(
        self,
        resource_type: str,
        product_name: str,
        resource_name: str,
        create_args: Dict,
        create_args_eq_fn: Callable[[Dict[str, Any]], bool],
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        replace: bool = False,
        success_message: Optional[str] = None,
    ):
        project_name = project_name or launchflow.project
        environment_name = environment_name or launchflow.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        try:
            existing_resource = await self.resource_async_client.get(
                project_name=project_name,
                environment_name=environment_name,
                resource_name=resource_name,
                product_name_to_validate=product_name,
            )
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code != 404:
                raise
            existing_resource = None

        if existing_resource and existing_resource.status == "pending":
            # TODO Add ability to show users that it's in a pending state
            logging.debug(
                f"Resource '{resource_name}' already exists in a pending state"
            )
            return AsyncResourcePendingOp(
                entity_ref=f"{resource_type}(name={resource_name})",
                client=self.lf_client,
                operation_id=None,
                _op=None,
            )
        elif (
            existing_resource
            and existing_resource.status in ["ready", "failed"]
            and create_args_eq_fn(existing_resource.create_args)
        ):
            logging.debug(
                f"Resource '{resource_name}' already exists with the same create args"
            )
            return AsyncResourceNoOp(
                entity_ref=f"{resource_type}(name={resource_name})",
                client=self.lf_client,
                operation_id=None,
                _op=None,
            )

        elif existing_resource:
            if not replace:
                raise exceptions.ResourceReplacementRequired(resource_name)

            async def replace_operation():
                # NOTE: We attempt to clear the cache info when the op is applied, but
                # swallow any exceptions since its not critical to the operation
                maybe_clear_resource_cache(
                    project_name, environment_name, product_name, resource_name
                )
                return await self.resource_async_client.replace(
                    project_name=project_name,
                    environment_name=environment_name,
                    product_name=product_name,
                    resource_name=resource_name,
                    create_args=create_args,
                )

            return AsyncEntityOp(
                entity_ref=f"{resource_type}(name={resource_name})",
                operation_id=None,
                client=self.lf_client,
                _op=replace_operation,
                _type="replace",
                _create_args=create_args,
                _replace_args=existing_resource.create_args,
                success_message=success_message,
            )

        else:

            async def create_operation():
                # NOTE: We attempt to clear the cache info when the op is applied, but
                # swallow any exceptions since its not critical to the operation
                maybe_clear_resource_cache(
                    project_name, environment_name, product_name, resource_name
                )
                return await self.resource_async_client.create(
                    project_name=project_name,
                    environment_name=environment_name,
                    product_name=product_name,
                    resource_name=resource_name,
                    create_args=create_args,
                )

            return AsyncEntityOp(
                entity_ref=f"{resource_type}(name={resource_name})",
                operation_id=None,
                client=self.lf_client,
                _op=create_operation,
                _type="create",
                success_message=success_message,
            )

    async def deploy_service_operation_async(
        self,
        service_type: str,
        product_name: str,
        create_args: Dict[str, Any],
        dockerfile_path: str,
        build_directory: str,
        build_ignore: List[str],
        service_name: str,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        notify_on_failure: bool = False,
    ):
        project_name = project_name or launchflow.project
        environment_name = environment_name or launchflow.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        full_yaml_path = os.path.dirname(os.path.abspath(config.launchflow_yaml.path))
        build_directory = os.path.join(full_yaml_path, build_directory)
        tar_bytes = tar_source_in_memory(
            directory=build_directory,
            ignore_patterns=build_ignore,
        )

        async def deploy_operation():
            return await self.service_async_client.deploy(
                service_name=service_name,
                project_name=project_name,
                environment_name=environment_name,
                product_name=product_name,
                dockerfile_path=dockerfile_path,
                create_args=create_args,
                tar_bytes=tar_bytes,
                notify_on_failure=notify_on_failure,
            )

        return AsyncEntityOp(
            entity_ref=f"{service_type}(name={service_name})",
            operation_id=None,
            client=self.lf_client,
            _op=deploy_operation,
            _type="deploy",
            _create_args=create_args,
        )

    async def promote_service_operation_async(
        self,
        service_type: str,
        create_args: Dict[str, Any],
        service_name: str,
        from_environment_name: Optional[str],
        to_environment_name: Optional[str],
        project_name: Optional[str] = None,
        notify_on_failure: bool = False,
    ):
        project_name = project_name or launchflow.project

        async def promote_operation():
            return await self.service_async_client.promote(
                service_name=service_name,
                project_name=project_name,
                from_environment_name=from_environment_name,
                to_environment_name=to_environment_name,
                create_args=create_args,
                notify_on_failure=notify_on_failure,
            )

        return AsyncEntityOp(
            entity_ref=f"{service_type}(name={service_name})",
            operation_id=None,
            client=self.lf_client,
            _op=promote_operation,
            _type="promote",
            _create_args=create_args,
        )

    def get_gcp_service_account_email(
        self,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
    ):
        project_name = project_name or launchflow.project
        environment_name = environment_name or launchflow.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        gcp_service_account_email = _load_gcp_service_account_email_from_cache(
            project_name, environment_name
        )

        if gcp_service_account_email is None:
            environment_info = self.environment_sync_client.get(
                project_name=project_name, env_name=environment_name
            )
            if environment_info.gcp_config is None:
                raise exceptions.GCPConfigNotFound(environment_name)
            gcp_service_account_email = (
                environment_info.gcp_config.gcp_service_account_email
            )
            cache.set_gcp_service_account_email(
                project_name, environment_name, gcp_service_account_email
            )

        return gcp_service_account_email
