from typing import Optional

from pydantic import BaseModel

from launchflow.models.enums import EnvironmentType


class AWSEnvironmentCreationInputs(BaseModel):
    launchflow_project_name: str
    launchflow_environment_name: str
    aws_account_id: str
    region: str
    environment_type: EnvironmentType
    artifact_bucket: Optional[str]
    lock_id: str


class AWSEnvironmentCreationOutputs(BaseModel):
    vpc_id: Optional[str]
    role_arn: Optional[str]
    policy_arn: Optional[str]
    ecs_cluster_name: Optional[str]
    artifact_bucket: Optional[str]
    success: bool
