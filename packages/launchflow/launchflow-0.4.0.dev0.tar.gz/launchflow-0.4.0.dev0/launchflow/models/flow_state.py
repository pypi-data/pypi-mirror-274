import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from launchflow.models.enums import (
    CloudProvider,
    EnvironmentType,
    ResourceProduct,
    ServiceProduct,
)


class _Entity(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GCPEnvironmentConfig(BaseModel):
    project_id: Optional[str]
    default_region: str
    default_zone: str
    service_account_email: Optional[str]
    artifact_bucket: Optional[str]


class AWSEnvironmentConfig(BaseModel):
    account_id: str
    region: str
    iam_role_arn: Optional[str]
    iam_policy_arn: Optional[str]
    vpc_id: Optional[str]
    ecs_cluster_name: Optional[str]
    artifact_bucket: Optional[str]


# TODO: Added name to this, might as well add name to everything?
class Resource(_Entity):
    name: str
    cloud_provider: CloudProvider
    product: ResourceProduct
    gcp_id: Optional[str] = None
    aws_arn: Optional[str] = None
    create_args: Dict[str, Any] = None

    def to_dict(self):
        return self.model_dump(
            mode="json", exclude_defaults=True, exclude=["environments"]
        )


class Service(_Entity):
    cloud_provider: CloudProvider
    product: ServiceProduct
    gcp_id: Optional[str] = None
    aws_arn: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    service_url: Optional[str] = None
    docker_image: Optional[str] = None

    def to_dict(self):
        return self.model_dump(mode="json", exclude_defaults=True)


class Environment(_Entity):
    environment_type: EnvironmentType
    ready: bool
    resources: Dict[str, Resource] = Field(default_factory=dict)
    services: Dict[str, Service] = Field(default_factory=dict)
    gcp_config: Optional[GCPEnvironmentConfig] = None
    aws_config: Optional[AWSEnvironmentConfig] = None
    ready: bool = True

    def to_dict(self):
        return self.model_dump(
            mode="json", exclude_defaults=True, exclude=["resources", "services"]
        )


class FlowState(_Entity):
    name: str
    environments: Dict[str, Environment] = Field(default_factory=dict)

    def to_dict(self):
        return self.model_dump(
            mode="json", exclude_defaults=True, exclude=["environments"]
        )
