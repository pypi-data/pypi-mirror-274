import dataclasses
import json
import os
import uuid
from typing import Optional, Union

import httpx

from launchflow import config, exceptions
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.gcp_clients import get_storage_client


@dataclasses.dataclass
class LockInfo:
    lock_id: str
    # TODO: should probably make this an enum
    lock_operation: str


class Lock:

    def __init__(self) -> None:
        self._lock_info = None

    async def acquire(self) -> LockInfo:
        raise NotImplementedError

    async def release(self, lock_id: str) -> None:
        raise NotImplementedError

    async def __aenter__(self) -> LockInfo:
        self._lock_info = await self.acquire()
        return self._lock_info

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            await self.release(self._lock_info.lock_id)
        except FileNotFoundError:
            # Swallow the error if the lock file is missing
            # this means the lock has already been released.
            # This can happen if a directory is deleted for example
            # when an environment is deleted.
            pass


class LocalLock(Lock):

    def __init__(self, file_path: str, operation: str) -> None:
        self.file_path = file_path
        self.operation = operation

    async def acquire(self) -> LockInfo:
        try:
            lock_info = LockInfo(str(uuid.uuid4()), self.operation)
            if not os.path.exists(self.file_path):
                os.makedirs(self.file_path)
            with open(os.path.join(self.file_path, "flow.lock"), "x") as f:
                json.dump(dataclasses.asdict(lock_info), f)
            return lock_info
        except FileExistsError:
            raise exceptions.EntityLocked(self.file_path)

    async def release(self, lock_id: str) -> None:
        with open(os.path.join(self.file_path, "flow.lock"), "r") as f:
            lock = LockInfo(**json.load(f))
            if lock.lock_id == lock_id:
                os.remove(os.path.join(self.file_path, "flow.lock"))
            else:
                raise exceptions.LockMismatch(self.file_path)


class GCSLock(Lock):

    def __init__(
        self, bucket: str, prefix: str, entity_file_path: str, operation: str
    ) -> None:
        self.bucket = bucket
        self.prefix = prefix
        # TODO: maybe operation should be move to the aquire method instead
        self.operation = operation
        self.entity_file_path = entity_file_path
        self.lock_path = os.path.join(self.prefix, self.entity_file_path, "flow.lock")

    async def acquire(self) -> LockInfo:
        """Acquire a lock in GCS.

        The basic algorithm is:
        1. Create a blob with `if_generation_match=0`
        2. If this fails we know the lock already exists
        3. Return the lock info to the caller to allow them to unlock
        """
        try:
            from google.api_core.exceptions import PreconditionFailed
        except ImportError:
            raise exceptions.MissingGCPDependency()
        try:
            lock_info = LockInfo(str(uuid.uuid4()), self.operation)
            client = get_storage_client()
            bucket = client.bucket(self.bucket)
            blob = bucket.blob(self.lock_path)
            blob.upload_from_string(
                json.dumps(dataclasses.asdict(lock_info)),
                if_generation_match=0,
            )
            return lock_info
        except PreconditionFailed:
            raise exceptions.EntityLocked(self.entity_file_path)

    async def release(self, lock_id: str) -> None:
        """Release the lock from GCS.

        The basic algorithm is:
        1. Download the lock file
        2. Verify the client unlocking is the same as the client locking
        3. Delete the lock file to release the lock
        """
        read_lock_info = await self.read_lock()
        if read_lock_info is None:
            # Swallow the error if the lock file is missing
            return
        if read_lock_info.lock_id == lock_id:
            client = get_storage_client()
            bucket = client.bucket(self.bucket)
            blob = bucket.blob(self.lock_path)
            blob.delete()

    async def read_lock(self) -> LockInfo:
        try:
            from google.api_core.exceptions import NotFound
        except ImportError:
            raise exceptions.MissingGCPDependency()
        client = get_storage_client()
        bucket = client.bucket(self.bucket)
        blob = bucket.blob(self.lock_path)
        try:
            remote_lock_info = LockInfo(**json.loads(blob.download_as_string()))
            return remote_lock_info
        except NotFound:
            return


class LaunchFlowLock(Lock):

    def __init__(
        self,
        project: str,
        entity_path: str,
        operation: str,
        launch_url: str,
        launchflow_api_key: Optional[str],
    ) -> None:
        self.project = project
        self.entity_path = entity_path
        launch_service_url = (
            f"{launch_url}/v2/projects/{self.project}/{self.entity_path}"
        )
        self.lock_url = f"{launch_service_url}/lock"
        self.unlock_url = f"{launch_service_url}/unlock"
        self.operation = operation
        self.launchflow_api_key = launchflow_api_key

    def get_access_token(self) -> str:
        if self.launchflow_api_key is not None:
            return self.launchflow_api_key
        else:
            return config.get_access_token()

    async def acquire(self) -> LockInfo:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.lock_url,
                json={"operation": self.operation},
                headers={"Authorization": f"Bearer {self.get_access_token()}"},
            )
            if response.status_code != 200:
                raise exceptions.LaunchFlowRequestFailure(response)
            return LockInfo(**response.json())

    async def release(self, lock_id: str) -> None:
        # TODO: probably want to add some retries to make sure this always works
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.unlock_url,
                json={"lock_id": lock_id},
                headers={"Authorization": f"Bearer {self.get_access_token()}"},
            )
            if response.status_code != 200:
                raise exceptions.LaunchFlowRequestFailure(response)


def lock_environment(
    backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
    env_name: str,
    operation: str,
) -> LocalLock:
    if isinstance(backend, LocalBackend):
        env_path = os.path.join(backend.path, env_name)
        return LocalLock(env_path, operation)
    elif isinstance(backend, GCSBackend):
        return GCSLock(backend.bucket, backend.prefix, env_name, operation)
    elif isinstance(backend, LaunchFlowBackend):
        return LaunchFlowLock(
            project=config.project,
            entity_path=f"environments/{env_name}",
            operation=operation,
        )
    else:
        raise NotImplementedError("Only local backend is supported")
