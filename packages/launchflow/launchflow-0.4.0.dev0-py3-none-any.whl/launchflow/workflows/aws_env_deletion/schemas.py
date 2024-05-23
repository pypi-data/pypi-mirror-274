from pydantic import BaseModel


class AWSEnvironmentDeletionInputs(BaseModel):
    launchflow_project_name: str
    launchflow_environment_name: str
    aws_account_id: str
    artifact_bucket: str
    lock_id: str


class AWSEnvironmentDeletionOutputs(BaseModel):
    success: bool
