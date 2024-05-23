from typing import Optional

import httpx

from launchflow.clients.response_schemas import OperationResponse
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.models.flow_state import Environment


class EnvironmentsSyncClient:
    def __init__(self, http_client: httpx.Client, api_key: Optional[str] = None):
        self.http_client = http_client
        self._api_key = api_key

    @property
    def access_token(self):
        if self._api_key is not None:
            return self._api_key
        else:
            return config.get_access_token()

    def base_url(self, project_name: str) -> str:
        return f"{config.settings.launch_service_address}/v2/projects/{project_name}/environments"

    def create(
        self,
        project_name: str,
        env_name: str,
        environment: Environment,
        lock_id: str,
    ) -> OperationResponse:
        body = {
            "name": env_name,
            "flow_state_environment": environment.model_dump(mode="json"),
            "lock_id": lock_id,
        }
        response = self.http_client.post(
            f"{self.base_url(project_name)}",
            json=body,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return Environment.model_validate(response.json())

    def get(self, project_name: str, env_name: str) -> Environment:
        url = f"{self.base_url(project_name)}/{env_name}"
        response = self.http_client.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return Environment.model_validate(response.json())

    def list(self, project_name: str):
        response = self.http_client.get(
            self.base_url(project_name),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return {
            name: Environment.model_validate(env)
            for name, env in response.json()["environments"].items()
        }

    def delete(self, project_name: str, env_name: str, lock_id: str):
        url = f"{self.base_url(project_name)}/{env_name}?lock_id={lock_id}"
        response = self.http_client.delete(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return response.json()


class EnvironmentsAsyncClient:
    def __init__(
        self,
        http_client: httpx.AsyncClient,
        launch_service_url: str,
        api_key: Optional[str] = None,
    ):
        self.http_client = http_client
        self._launch_service_url = launch_service_url
        self._api_key = api_key

    @property
    def access_token(self):
        if self._api_key is not None:
            return self._api_key
        else:
            return config.get_access_token()

    def base_url(self, project_name: str) -> str:
        return f"{self._launch_service_url}/v2/projects/{project_name}/environments"

    async def create(
        self,
        project_name: str,
        env_name: str,
        environment: Environment,
        lock_id: str,
    ) -> OperationResponse:
        body = {
            "name": env_name,
            "flow_state_environment": environment.to_dict(),
            "lock_id": lock_id,
        }
        response = await self.http_client.post(
            f"{self.base_url(project_name)}",
            json=body,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return Environment.model_validate(response.json())

    async def get(self, project_name: str, env_name: str) -> Environment:
        url = f"{self.base_url(project_name)}/{env_name}"
        response = await self.http_client.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return Environment.model_validate(response.json())

    async def list(self, project_name):
        response = await self.http_client.get(
            self.base_url(project_name),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return {
            name: Environment.model_validate(env)
            for name, env in response.json()["environments"].items()
        }

    async def delete(self, project_name: str, env_name: str, lock_id: str):
        url = f"{self.base_url(project_name)}/{env_name}?lock_id={lock_id}"
        response = await self.http_client.delete(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return response.json()
