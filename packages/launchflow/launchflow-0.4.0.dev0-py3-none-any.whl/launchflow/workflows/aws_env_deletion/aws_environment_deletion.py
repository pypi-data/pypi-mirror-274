
from launchflow import config, exceptions
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.workflows.aws_env_deletion.schemas import AWSEnvironmentDeletionInputs
from launchflow.workflows.commands.tf_commands import TFDestroyCommand
from launchflow.workflows.utils import run_tofu


def _delete_artifact_bucket(bucket_name: str):
    try:
        import boto3
        import botocore
    except ImportError:
        raise exceptions.MissingAWSDependency()
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    try:
        # First delete all objects in the bucket
        bucket.objects.all().delete()
        # Then delete the bucket
        bucket.delete()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            return
        raise


async def _run_tofu(inputs: AWSEnvironmentDeletionInputs):
    if isinstance(config.launchflow_yaml.backend, LocalBackend):
        state_prefix = f"{config.launchflow_yaml.backend.path}/{inputs.launchflow_environment_name}"
    elif isinstance(config.launchflow_yaml.backend, GCSBackend):
        state_prefix = f"{config.launchflow_yaml.backend.prefix}/{inputs.launchflow_environment_name}"
    elif isinstance(config.launchflow_yaml.backend, LaunchFlowBackend):
        state_prefix = f"{inputs.launchflow_project_name}/environments/{inputs.launchflow_environment_name}/tofu-state?lock_id={inputs.lock_id}"
    else:
        raise ValueError("Only local backend is supported")
    command = TFDestroyCommand(
        tf_module_dir="workflows/tf/empty/aws_empty",
        backend=config.launchflow_yaml.backend,
        tf_state_prefix=state_prefix,
        tf_vars={
            "aws_account_id": inputs.aws_account_id,
        },
    )
    return await run_tofu(command)


async def delete_aws_environment(inputs: AWSEnvironmentDeletionInputs):
    _delete_artifact_bucket(inputs.artifact_bucket)
    return await _run_tofu(inputs)
