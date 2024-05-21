from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Dict, Literal, Optional

from docker.models.containers import Container
from launchflow.clients.client import LaunchFlowAsyncClient
from launchflow.clients.response_schemas import OperationResponse, OperationStatus

from launchflow import exceptions


@dataclass
class AsyncOp:
    operation_id: Optional[str]
    client: LaunchFlowAsyncClient
    _op: Callable[[], Coroutine[None, None, OperationResponse]]

    async def run(self):
        if self.operation_id is not None:
            raise exceptions.OperationAlreadyStarted(str(self))

        operation = await self._op()
        self.operation_id = operation.id

    async def stream_status(self):
        if self.operation_id is None:
            raise exceptions.OperationNotStarted(str(self))
        async for status in self.client.operations.stream_operation_status(
            self.operation_id
        ):
            yield status

    async def get_status(self) -> OperationStatus:
        if self.operation_id is None:
            raise exceptions.OperationNotStarted(str(self))
        return await self.client.operations.get_operation_status(self.operation_id)

    async def done(self):
        return (await self.get_status()).is_final()

    async def result(self) -> str:
        # starts and blocks until the operation is done
        await self.run()
        async for status in self.stream_status():
            if status.is_final():
                return status


@dataclass
class AsyncEntityOp(AsyncOp):
    entity_ref: str

    _type: Literal["create", "replace", "deploy"]
    # Resource for the entity, set to none if the operation is not related to a resource
    # TODO: fix circular import
    resource: Optional[Any] = None
    success_message: Optional[str] = None
    _create_args: Optional[Dict] = None
    _replace_args: Optional[Dict] = None


@dataclass
class AsyncResourceNoOp(AsyncEntityOp):
    _type: Literal["noop", "pending"] = "noop"

    async def run(self):
        pass

    async def stream_status(self):
        yield OperationStatus.SUCCESS

    async def get_status(self):
        return OperationStatus.SUCCESS

    async def done(self):
        return True

    async def result(self):
        return OperationStatus.SUCCESS


@dataclass
class AsyncResourcePendingOp(AsyncEntityOp):
    _type: Literal["noop", "pending"] = "pending"

    async def stream_status(self):
        yield OperationStatus.FAILURE

    async def get_status(self):
        return OperationStatus.FAILURE

    async def done(self):
        return True

    async def result(self):
        return OperationStatus.FAILURE


@dataclass
class AsyncDockerOp:
    container: Optional[Container]
    _op: Callable[[], Coroutine[None, None, Optional[Container]]]

    def __post_init__(self):
        self.operation_id = "docker_op"

    async def run(self):
        if self.container is not None:
            raise exceptions.OperationAlreadyStarted(str(self))
        container = await self._op()
        self.container = container

    async def stream_status(self):
        if self.container is None:
            raise exceptions.OperationNotStarted(str(self))
        if self.container.status == "running":
            yield OperationStatus.SUCCESS
        else:
            yield OperationStatus.FAILURE

    async def get_status(self) -> OperationStatus:
        if self.container is None:
            raise exceptions.OperationNotStarted(str(self))
        # refresh the container status
        self.container.reload()
        if self.container.status == "created":
            return OperationStatus.PENDING
        elif self.container.status == "running":
            return OperationStatus.SUCCESS
        return OperationStatus.FAILURE

    async def done(self):
        return self.container is not None and self.container.status == "running"

    async def result(self) -> str:
        # starts and blocks until the operation is done
        await self.run()
        async for status in self.stream_status():
            if status.is_final():
                return status


@dataclass
class AsyncDockerResourceOp(AsyncDockerOp):
    entity_ref: str
    _type: Literal["create", "replace"]
    _create_args: Optional[Dict] = None
    _replace_args: Optional[Dict] = None
    resource: Optional[Any] = None
    success_message: Optional[str] = None


@dataclass
class AsyncDockerResourceNoOp(AsyncDockerOp):
    entity_ref: str
    _type: Literal["noop"] = "noop"

    async def run(self):
        pass

    async def stream_status(self):
        yield OperationStatus.SUCCESS

    async def get_status(self):
        return OperationStatus.SUCCESS

    async def done(self):
        return True

    async def result(self):
        return OperationStatus.SUCCESS
