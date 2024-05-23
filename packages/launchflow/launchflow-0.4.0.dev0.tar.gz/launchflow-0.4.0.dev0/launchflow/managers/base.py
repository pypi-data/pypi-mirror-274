from typing import Optional, Union

from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)


class BaseManager:

    def __init__(
        self,
        backend: Union[LocalBackend, LaunchFlowBackend, GCSBackend],
        launchflow_api_key: Optional[str] = None,
        launchflow_backend_url: Optional[str] = None,
    ) -> None:
        self.backend = backend
        self.launchflow_api_key = launchflow_api_key
        self.launchflow_backend_url = launchflow_backend_url
