import logging

from pydantic import BaseModel

from launchflow import exceptions
from launchflow.config import config
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.workflows.aws_env_creation.schemas import (
    AWSEnvironmentCreationInputs,
    AWSEnvironmentCreationOutputs,
)
from launchflow.workflows.commands.tf_commands import TFApplyCommand
from launchflow.workflows.utils import run_tofu, unique_resource_name_generator


class _AWSTofuOutputs(BaseModel):
    vpc_id: str
    role_arn: str
    policy_arn: str
    ecs_cluster_name: str
    success: bool


async def _create_artifact_bucket(project_name: str, environment_name: str):
    try:
        import boto3
    except ImportError:
        # TODO: make this a better exception
        raise exceptions.MissingAWSDependency()
    s3_client = boto3.client("s3")
    bucket_name = f"{project_name}-{environment_name}-artifacts"
    for unique_bucket_name in unique_resource_name_generator(bucket_name):
        try:
            s3_client.create_bucket(Bucket=unique_bucket_name)
            break
        except s3_client.exceptions.BucketAlreadyExists:
            continue
    s3_client.put_bucket_lifecycle_configuration(
        Bucket=unique_bucket_name,
        LifecycleConfiguration={
            "Rules": [
                {
                    "ID": "log-file-expiration",
                    # TODO: make this configurable
                    "Expiration": {"Days": 14},
                    "Filter": {"Prefix": "logs/"},
                    "Status": "Enabled",
                }
            ]
        },
    )
    return unique_bucket_name


async def _run_tofu(
    inputs: AWSEnvironmentCreationInputs, artifact_bucket: str
) -> _AWSTofuOutputs:
    if isinstance(config.launchflow_yaml.backend, LocalBackend):
        state_prefix = f"{config.launchflow_yaml.backend.path}/{inputs.launchflow_environment_name}"
    elif isinstance(config.launchflow_yaml.backend, GCSBackend):
        state_prefix = f"{config.launchflow_yaml.backend.prefix}/{inputs.launchflow_environment_name}"
    elif isinstance(config.launchflow_yaml.backend, LaunchFlowBackend):
        state_prefix = f"{inputs.launchflow_project_name}/environments/{inputs.launchflow_environment_name}/tofu-state?lock_id={inputs.lock_id}"
    else:
        raise ValueError("Only local backend is supported")
    command = TFApplyCommand(
        tf_module_dir="workflows/tf/environments/aws",
        backend=config.launchflow_yaml.backend,
        tf_state_prefix=state_prefix,
        # TODO: add tf_vars
        tf_vars={
            "aws_region": inputs.region,
            "launchflow_project": inputs.launchflow_project_name,
            "launchflow_environment": inputs.launchflow_environment_name,
            "aws_account_id": inputs.aws_account_id,
            "artifact_bucket_name": artifact_bucket,
        },
    )
    tf_outputs = await run_tofu(command)
    return _AWSTofuOutputs(
        vpc_id=tf_outputs["vpc_id"],
        role_arn=tf_outputs["role_arn"],
        policy_arn=tf_outputs["policy_arn"],
        ecs_cluster_name=tf_outputs["ecs_cluster_name"],
        success=True,
    )


async def create_aws_environment(
    inputs: AWSEnvironmentCreationInputs,
) -> AWSEnvironmentCreationOutputs:
    artifact_bucket = None
    vpc_id = None
    role_arn = None
    policy_arn = None
    ecs_cluster_name = None
    success = True
    try:
        if inputs.artifact_bucket is None:
            artifact_bucket = await _create_artifact_bucket(
                inputs.launchflow_project_name, inputs.launchflow_environment_name
            )
        else:
            artifact_bucket = inputs.artifact_bucket

        outputs = await _run_tofu(inputs, artifact_bucket)
        vpc_id = outputs.vpc_id
        role_arn = outputs.role_arn
        policy_arn = outputs.policy_arn
        ecs_cluster_name = outputs.ecs_cluster_name
    except Exception:
        logging.exception("Error creating AWS environment")
        success = False

    return AWSEnvironmentCreationOutputs(
        vpc_id=vpc_id,
        role_arn=role_arn,
        policy_arn=policy_arn,
        ecs_cluster_name=ecs_cluster_name,
        artifact_bucket=artifact_bucket,
        success=success,
    )
