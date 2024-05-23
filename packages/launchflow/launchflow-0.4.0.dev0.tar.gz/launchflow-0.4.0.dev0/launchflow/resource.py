import asyncio
import datetime
import tempfile
from typing import Any, Dict, Generic, TypeVar, get_args

from pydantic import BaseModel

from launchflow.context import LaunchFlowContext
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.managers.resource_manager import ResourceManager
from launchflow.models.enums import CloudProvider, ResourceProduct
from launchflow.models.flow_state import Resource as FlowStateResource
from launchflow.workflows.tf.tf import AWSTF, GCPTF
from launchflow.workflows.tf.tf_utils import resource_to_tf

T = TypeVar("T", bound=BaseModel)


# TODO: Add autodocs / examples for this class
class Resource(Generic[T]):
    def __init__(self, name: str, product_name: str, create_args: Dict[str, Any]):
        self.name = name
        self._product_name = product_name
        self._create_args = create_args

        # This line extracts the type argument from the Generic base
        self._connection_type: T = get_args(self.__class__.__orig_bases__[0])[0]
        self._success_message = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    @property
    def product_name(self) -> str:
        """Product name property.

        Returns:
        - The product name.
        """
        return self._product_name

    def connect(self):
        """
        Synchronously connect to the resource by fetching its connection info.
        """
        context = LaunchFlowContext()
        connection_info = context.get_resource_connection_info_sync(
            product_name=self._product_name,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    async def connect_async(self):
        """
        Asynchronously connect to the resource by fetching its connection info.
        """
        context = LaunchFlowContext()
        connection_info = await context.get_resource_connection_info_async(
            product_name=self._product_name,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    def create(
        self,
        *,
        environment_manager: EnvironmentManager,
        resource_manager: ResourceManager,
        replace: bool = False,
    ):
        """
        Synchronously create the resource.
        """
        return asyncio.run(
            self.create_async(
                environment_manager=environment_manager,
                resource_manager=resource_manager,
                replace=replace,
            )
        )


    async def create_async(
        self,
        *,
        environment_manager: EnvironmentManager,
        resource_manager: ResourceManager,
        replace: bool = False,
    ):
        """
        Asynchronously create the resource.
        """
        environment = await environment_manager.load_environment()

        # Lock the environment while grabbing the resource lock, but immediately release it
        async with environment_manager.lock_environment("update"):
            resource_lock = resource_manager.lock_resource("create")

        async with resource_lock as resource_lock_info:
            resource_tf = resource_to_tf(self, environment)
            tf_apply = resource_tf.to_tf_apply_command(environment_manager.environment_name)

            with tempfile.TemporaryDirectory() as tempdir:
                tf_outputs = await tf_apply.run(tempdir)

            if isinstance(resource_tf, GCPTF):
                cloud_provider = CloudProvider.GCP
            elif isinstance(resource_tf, AWSTF):
                cloud_provider = CloudProvider.AWS
            else:
                raise NotImplementedError

            now = datetime.datetime.now()

            resource_flow_state = FlowStateResource(
                name=self.name,
                cloud_provider=cloud_provider,
                created_at=now,
                updated_at=now,
                product=ResourceProduct[self.product_name.upper()],
                gcp_id=tf_outputs["gcp_id"],
                create_args=self._create_args
            )

            await resource_manager.save_resource(resource_flow_state, resource_lock_info.lock_id)
