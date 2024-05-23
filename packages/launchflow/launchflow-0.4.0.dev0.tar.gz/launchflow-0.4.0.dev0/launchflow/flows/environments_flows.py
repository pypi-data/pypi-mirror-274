import datetime
from typing import Optional

import beaupy
import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow import exceptions
from launchflow.clients.response_schemas import EnvironmentType
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.managers.flow_state_manager import FlowStateManager
from launchflow.models.enums import CloudProvider
from launchflow.models.flow_state import (
    AWSEnvironmentConfig,
    Environment,
    GCPEnvironmentConfig,
)
from launchflow.validation import validate_environment_name
from launchflow.workflows import (
    AWSEnvironmentCreationInputs,
    AWSEnvironmentDeletionInputs,
    GCPEnvironmentCreationInputs,
    GCPEnvironmentDeletionInputs,
    create_aws_environment,
    create_gcp_environment,
    delete_aws_environment,
    delete_gcp_environment,
)


async def get_environment(
    flow_state_manager: FlowStateManager,
    environment_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    # TODO: what do we do about local
    # if environment_name == "local":
    #     return EnvironmentResponse(
    #         name="local",
    #         environment_type=EnvironmentType.LOCAL,
    #         created_at=datetime.datetime.now(),
    #         updated_at=datetime.datetime.now(),
    #         status="active",
    #         status_message="",
    #     )
    if environment_name is None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Fetching environments...", total=None)
            environments = await flow_state_manager.list_environments()
            progress.remove_task(task)
        environment_names = [f"{name}" for name in environments.items()]
        if prompt_for_creation:
            environment_names.append("[i yellow]Create new environment[/i yellow]")
        print("Select the environment to use:")
        selected_environment = beaupy.select(environment_names, strict=True)
        if prompt_for_creation and selected_environment == environment_names[-1]:
            if environment_name is None:
                environment_name = beaupy.prompt("Enter the environment name:")
                rich.print(f"[pink1]>[/pink1] {environment_name}")
            validate_environment_name(environment_name)
            environment = await create_environment(
                environment_type=None,
                cloud_provider=None,
                manager=EnvironmentManager(
                    project_name=flow_state_manager.project_name,
                    environment_name=environment_name,
                    backend=flow_state_manager.backend,
                ),
            )
        else:
            rich.print(f"[pink1]>[/pink1] {environment_name}")
            environment = environments[selected_environment]
        return environment
    try:
        # Fetch the environment to ensure it exists
        env_manager = EnvironmentManager(
            project_name=flow_state_manager.project_name,
            environment_name=environment_name,
            backend=flow_state_manager.backend,
        )
        environment = await env_manager.load_environment()
    except exceptions.EnvironmentNotFound as e:
        if prompt_for_creation:
            answer = beaupy.confirm(
                f"Environment `{environment_name}` does not exist yet. Would you like to create it?"
            )
            if answer:
                environment = await create_environment(
                    environment_type=None,
                    cloud_provider=None,
                    manager=EnvironmentManager(
                        project_name=flow_state_manager.project_name,
                        environment_name=environment_name,
                        backend=flow_state_manager.backend,
                    ),
                )
            else:
                raise e
        else:
            raise e
    return environment


async def delete_environment(manager: EnvironmentManager, detach: bool = False):
    async with manager.lock_environment(operation="delete") as lock:
        existing_environment = await manager.load_environment()
        if not detach:
            if existing_environment.gcp_config is not None:
                await delete_gcp_environment(
                    inputs=GCPEnvironmentDeletionInputs(
                        launchflow_project_name=manager.project_name,
                        launchflow_environment_name=manager.environment_name,
                        environment=existing_environment,
                    )
                )
            elif existing_environment.aws_config is not None:
                await delete_aws_environment(
                    inputs=AWSEnvironmentDeletionInputs(
                        launchflow_project_name=manager.project_name,
                        launchflow_environment_name=manager.environment_name,
                        aws_account_id=existing_environment.aws_config.account_id,
                        artifact_bucket=existing_environment.aws_config.artifact_bucket,
                        lock_id=lock.lock_id,
                    )
                )
        await manager.delete_environment(lock.lock_id)


async def create_environment(
    environment_type: Optional[EnvironmentType],
    cloud_provider: Optional[CloudProvider],
    manager: EnvironmentManager,
) -> Optional[Environment]:
    """Create a new environment in a project."""
    async with manager.lock_environment(operation="create") as lock:
        # TODO: maybe prompt the user if the environment already exists that this will update stuff
        try:
            existing_environment = await manager.load_environment()
        except exceptions.EnvironmentNotFound:
            existing_environment = None
        if existing_environment is not None:
            existing_environment_type = existing_environment.environment_type
            if (
                environment_type is not None
                and environment_type != existing_environment_type
            ):
                raise exceptions.ExistingEnvironmentDifferentEnvironmentType(
                    manager.environment_name, existing_environment_type
                )
            environment_type = existing_environment_type

            existing_cloud_provider = None
            if existing_environment.aws_config is not None:
                existing_cloud_provider = CloudProvider.AWS
            elif existing_environment.gcp_config is not None:
                existing_cloud_provider = CloudProvider.GCP
            else:
                raise ValueError("Environment has no cloud provider.")
            if cloud_provider is not None and cloud_provider != existing_cloud_provider:
                raise exceptions.ExistingEnvironmentDifferentCloudProvider(
                    manager.environment_name
                )

            cloud_provider = existing_cloud_provider

        if environment_type is None:
            print("Select the environment type:")
            selection = beaupy.select(
                ["development", "production"],
                strict=True,
            )
            rich.print(f"[pink1]>[/pink1] {selection}")
            environment_type = EnvironmentType(selection)
            print()

        if cloud_provider is None:
            print("Select the cloud provider for the environment:")
            selection = beaupy.select(["GCP", "AWS"], strict=True)
            rich.print(f"[pink1]>[/pink1] {selection}")
            cloud_provider = CloudProvider[selection]
            print()

        if cloud_provider == CloudProvider.GCP:
            gcp_environment_info = await create_gcp_environment(
                inputs=GCPEnvironmentCreationInputs(
                    launchflow_project_name=manager.project_name,
                    launchflow_environment_name=manager.environment_name,
                    gcp_project_id=(
                        existing_environment.gcp_config.project_id
                        if existing_environment
                        else None
                    ),
                    environment_service_account_email=(
                        existing_environment.gcp_config.service_account_email
                        if existing_environment
                        else None
                    ),
                    artifact_bucket=(
                        existing_environment.gcp_config.artifact_bucket
                        if existing_environment
                        else None
                    ),
                    lock_id=lock.lock_id,
                ),
            )
            create_time = datetime.datetime.now(datetime.timezone.utc)
            env = Environment(
                name=manager.environment_name,
                created_at=create_time,
                updated_at=create_time,
                gcp_config=GCPEnvironmentConfig(
                    project_id=gcp_environment_info.gcp_project_id,
                    default_region="us-central1",
                    default_zone="us-central1-a",
                    service_account_email=gcp_environment_info.environment_service_account_email,
                    artifact_bucket=gcp_environment_info.artifact_bucket,
                ),
                environment_type=environment_type,
                ready=gcp_environment_info.success,
            )
        elif cloud_provider == CloudProvider.AWS:

            if existing_environment is not None:
                aws_account_id = existing_environment.aws_config.account_id
                region = existing_environment.aws_config.region
            else:
                try:
                    import boto3
                    import botocore
                except ImportError:
                    raise exceptions.MissingAWSDependency()
                sts = boto3.client("sts")
                try:
                    response = sts.get_caller_identity()
                    aws_account_id = response["Account"]
                except botocore.exceptions.NoCredentialsError as e:
                    raise exceptions.NoAWSCredentialsFound() from e

                answer = beaupy.confirm(
                    f"Based on your credentials this will create an environment in AWS account {aws_account_id}. Would you like to continue?"
                )
                if not answer:
                    typer.echo("AWS account ID rejected.")
                    typer.exit(1)

                # TODO: make this configurable
                region = "us-east-1"
            aws_environment_info = await create_aws_environment(
                inputs=AWSEnvironmentCreationInputs(
                    launchflow_project_name=manager.project_name,
                    launchflow_environment_name=manager.environment_name,
                    region=region,
                    aws_account_id=aws_account_id,
                    environment_type=environment_type,
                    artifact_bucket=(
                        existing_environment.aws_config.artifact_bucket
                        if existing_environment
                        else None
                    ),
                    lock_id=lock.lock_id,
                )
            )
            create_time = datetime.datetime.now(datetime.timezone.utc)
            env = Environment(
                name=manager.environment_name,
                created_at=create_time,
                updated_at=create_time,
                aws_config=AWSEnvironmentConfig(
                    artifact_bucket=aws_environment_info.artifact_bucket,
                    vpc_id=aws_environment_info.vpc_id,
                    iam_role_arn=aws_environment_info.role_arn,
                    iam_policy_arn=aws_environment_info.policy_arn,
                    ecs_cluster_name=aws_environment_info.ecs_cluster_name,
                    region=region,
                    account_id=aws_account_id,
                ),
                environment_type=environment_type,
                ready=aws_environment_info.success,
            )
        else:
            raise ValueError("Invalid cloud provider.")
        await manager.save_environment(env, lock.lock_id)
        if env.ready:
            rich.print("[green]Environment created successfully![/green]")
            return env
        else:
            rich.print("[red]✗ Failed to create environment.[/red]")
