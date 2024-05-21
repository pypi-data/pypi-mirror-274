import asyncio

import httpx
from launchflow.clients.response_schemas import OperationResponse, OperationStatus
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class OperationsAsyncClient:
    def __init__(self, http_client: httpx.AsyncClient, api_key: str):
        self.http_client = http_client
        self._api_key = api_key

    @property
    def access_token(self):
        if self._api_key is not None:
            return self._api_key
        else:
            return config.get_access_token()

    def base_url(self) -> str:
        return f"{config.settings.launch_service_address}/operations"

    # TODO: merge this into one stream_operation
    async def stream_operation_status(self, operation_id: str):
        operation_status = OperationStatus.UNKNOWN

        while True:
            operation = await self.get(operation_id)
            operation_status = operation.status

            if operation.status.is_final():
                break

            yield operation_status

            await asyncio.sleep(3)

        yield operation_status

    async def stream_operation_status_and_message(self, operation_id: str):
        operation_status = OperationStatus.UNKNOWN

        while True:
            operation = await self.get(operation_id)
            operation_status = operation.status
            message = operation.status_message

            if operation.status.is_final():
                break

            yield operation_status, message

            await asyncio.sleep(3)

        yield operation_status, message

    async def get_operation_status(self, operation_id: str):
        operation = await self.get(operation_id)
        return operation.status

    async def get(self, operation_id: str):
        response = await self.http_client.get(
            f"{self.base_url()}/{operation_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)

        return OperationResponse.model_validate(response.json())

    async def wait_for_operation(self, operation_id: str):
        async for _ in self.stream_operation_status(operation_id):
            pass
