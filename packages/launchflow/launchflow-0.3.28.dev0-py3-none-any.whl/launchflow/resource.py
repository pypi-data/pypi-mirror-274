import asyncio
from typing import Any, Dict, Generic, List, Optional, TypeVar, get_args

from launchflow.context import LaunchFlowContext
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ResourceDependency:

    def __init__(self, dependency: "Resource") -> None:
        self.dependency = dependency

    def resolve() -> Dict[str, Any]:
        pass


# TODO: Add autodocs / examples for this class
class Resource(Generic[T]):
    def __init__(
        self,
        name: str,
        product_name: str,
        create_args: Dict[str, Any],
        depends_on: Optional[List["Resource"]] = None,
    ):
        self.name = name
        self._product_name = product_name
        self._create_args = create_args
        self._depends_on = depends_on if depends_on is not None else []

        # This line extracts the type argument from the Generic base
        self._connection_type: T = get_args(self.__class__.__orig_bases__[0])[0]
        self._success_message = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def _create_args_eq(self, other_args: Dict[str, Any]) -> bool:
        """Create args equality comparison, the default case is normal equality.

        **Args**:
        - `other_args` (Dict[str, Any]): The other create args to compare against.

        **Returns**:
        - `bool`: Whether the create args are equal.
        """
        return self._create_args == other_args

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
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
    ):
        """
        Synchronously create the resource.
        """
        return asyncio.run(
            self.create_async(
                project_name=project_name,
                environment_name=environment_name,
                replace=replace,
            )
        )

    async def create_async(
        self,
        *,
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
        api_key: Optional[str] = None,
    ):
        """
        Asynchronously create the resource.
        """
        context = LaunchFlowContext(api_key=api_key)
        return await context.create_resource_operation_async(
            resource=self,
            project_name=project_name,
            environment_name=environment_name,
            replace=replace,
            success_message=self._success_message,
        )
