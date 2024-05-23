import dataclasses
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel

from launchflow.config import config
from launchflow.workflows.commands.tf_commands import TFApplyCommand, TFDestroyCommand

CR = TypeVar("CR", bound=BaseModel)


@dataclasses.dataclass
class LaunchflowURI:
    project_name: str
    environment_name: str
    resource_name: Optional[str] = None
    service_name: Optional[str] = None

    def __post_init__(self):
        if self.resource_name and self.service_name:
            raise ValueError("resource_name and service_name cannot be used together")

    def tf_state_prefix(self) -> str:
        if self.resource_name:
            return f"terraform/state/{self.project_name}/{self.environment_name}/resources/{self.resource_name}"
        if self.service_name:
            return f"terraform/state/{self.project_name}/{self.environment_name}/services/{self.service_name}"
        return (
            f"terraform/state/{self.project_name}/{self.environment_name}/environment/"
        )


@dataclasses.dataclass
class TF(Generic[CR]):
    resource_name: str
    artifact_bucket: str
    create_args: Dict[str, Any]

    @classmethod
    def production(cls, **kwargs):
        raise NotImplementedError("production method not implemented")

    @classmethod
    def development(cls, **kwargs):
        raise NotImplementedError("development method not implemented")

    def tf_cwd(self) -> str:
        raise NotImplementedError("tf_cwd method not implemented")

    def tf_vars(self) -> Dict[str, str]:
        raise NotImplementedError("tf_vars method not implemented")

    def to_tf_apply_command(self, environment_name: str) -> TFApplyCommand:
        raise NotImplementedError("to_tf_container method not implemented")

    def to_tf_destroy_command(self, environment_name: str) -> TFDestroyCommand:
        raise NotImplementedError("to_tf_container method not implemented")


@dataclasses.dataclass
class GCPTF(TF[CR]):
    # The user's gcp project info
    gcp_project_id: str
    gcp_region: str

    def to_tf_apply_command(self, environment_name: str) -> TFApplyCommand:
        state_prefix = f"{config.launchflow_yaml.backend.path}/{environment_name}/resources/{self.resource_name}"

        return TFApplyCommand(
            tf_module_dir=self.tf_cwd(),
            backend=config.launchflow_yaml.backend,
            tf_state_prefix=state_prefix,
            tf_vars=self.tf_vars(),
        )

    def to_tf_destroy_command(self, environment_name: str) -> TFDestroyCommand:
        state_prefix = f"{config.launchflow_yaml.backend.path}/{environment_name}/resources/{self.resource_name}"

        return TFDestroyCommand(
            tf_module_dir=self.tf_cwd(),
            backend=config.launchflow_yaml.backend,
            tf_state_prefix=state_prefix,
            tf_vars=self.tf_vars(),
        )


@dataclasses.dataclass
class AWSTF(TF[CR]):
    # The user's aws account info
    aws_region: str
    vpc_id: str
    # Used to create the creds for the tofu command
    aws_account_id: str
    aws_external_role_id: str
    aws_iam_role_arn: str

    def to_tf_apply_command(self, environment_name: str) -> TFApplyCommand:
        raise NotImplementedError
        # return TFApplyCommand(
        #     auth_method="aws",
        #     artifact_bucket=self.artifact_bucket,
        #     tf_module_dir=self.tf_cwd(),
        #     tf_state_prefix=self.launchflow_uri.tf_state_prefix(),
        #     tf_vars=self.tf_vars(),
        #     aws_account_id=self.aws_account_id,
        #     aws_external_role_id=self.aws_external_role_id,
        #     aws_iam_role_arn=self.aws_iam_role_arn,
        # )

    def to_tf_destroy_command(self, environment_name: str) -> TFDestroyCommand:
        raise NotImplementedError
        # return TFDestroyCommand(
        #     auth_method="aws",
        #     artifact_bucket=self.artifact_bucket,
        #     tf_module_dir=self.tf_cwd(),
        #     tf_state_prefix=self.launchflow_uri.tf_state_prefix(),
        #     aws_account_id=self.aws_account_id,
        #     aws_external_role_id=self.aws_external_role_id,
        #     aws_iam_role_arn=self.aws_iam_role_arn,
        #     tf_vars=self.tf_vars(),
        # )
