import logging

import beaupy
import rich
import rich.progress
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from launchflow import exceptions
from launchflow.config import config
from launchflow.config.launchflow_yaml import (
    GCSBackend,
    LaunchFlowBackend,
    LocalBackend,
)
from launchflow.workflows.commands.tf_commands import TFApplyCommand
from launchflow.workflows.gcp_env_creation.schemas import (
    GCPEnvironmentCreationInputs,
    GCPEnvironmentCreationOutputs,
)
from launchflow.workflows.utils import run_tofu, unique_resource_name_generator


async def lookup_organization():
    try:
        from google.cloud import resourcemanager_v3
    except ImportError:
        raise exceptions.MissingGCPDependency()
    organization_client = resourcemanager_v3.OrganizationsAsyncClient()

    orgs = await organization_client.search_organizations()
    org: resourcemanager_v3.Organization = None
    # 1. look up organiztaion for the project
    # We do this first to ensure it won't fail before creating the project
    all_orgs = []
    async for o in orgs:
        all_orgs.append(o)
    if not all_orgs:
        raise exceptions.NoOrgs()
    if len(all_orgs) > 1:
        print(
            "You have access to multiple organizations. Please select which one to use:"
        )
        org_options = [f"{o.display_name} ({o.name})" for o in all_orgs]
        org_idx = beaupy.select(org_options, return_index=True, strict=True)
        if org_idx is None:
            raise ValueError("No org selected")
        org = all_orgs[org_idx]
        rich.print(f"[pink1]>[/pink1] {org_options[org_idx]}")
        print()

    else:
        org = all_orgs[0]
    return org.name


async def lookup_billing_account():
    try:
        from google.cloud import billing
    except ImportError:
        raise exceptions.MissingGCPDependency()
    billing_client = billing.CloudBillingAsyncClient()
    billing_accounts = await billing_client.list_billing_accounts()
    billing_account = None
    # TODO: setup billing account selection
    async for b in billing_accounts:
        if billing_account is not None:
            raise exceptions.MultipleBillingAccounts()
        billing_account = b
    if billing_account is None:
        raise exceptions.NoBillingAccountAccess()
    return billing_account.name


async def _create_gcp_project(project_name: str, environment_name: str, org_name: str):
    try:
        from google.api_core.exceptions import AlreadyExists
        from google.cloud import resourcemanager_v3
    except ImportError:
        raise exceptions.MissingGCPDependency()
    projects_client = resourcemanager_v3.ProjectsAsyncClient()

    # NOTE: We continually try new project IDs until we find a unique one.
    gcp_project_name = f"{project_name}-{environment_name}"
    for gcp_project_id in unique_resource_name_generator(
        gcp_project_name, max_length=30
    ):
        try:
            operation = await projects_client.create_project(
                project=resourcemanager_v3.Project(
                    # TODO: we could do folders here to but :shrug:
                    parent=org_name,
                    project_id=gcp_project_id,
                    display_name=gcp_project_name[:30],
                )
            )
            await operation.result()
            break
        except AlreadyExists:
            continue
    return gcp_project_id


async def _assign_billing_project(gcp_project_id: str, billing_account_name: str):
    try:
        from google.cloud import billing
    except ImportError:
        raise exceptions.MissingGCPDependency()
    billing_client = billing.CloudBillingAsyncClient()
    await billing_client.update_project_billing_info(
        name=f"projects/{gcp_project_id}",
        project_billing_info=billing.ProjectBillingInfo(
            billing_account_name=billing_account_name,
        ),
    )


async def _maybe_create_default_network(gcp_project_id: str):
    try:
        from google.cloud import compute_v1, service_usage_v1
    except ImportError:
        raise exceptions.MissingGCPDependency()

    service_usage_client = service_usage_v1.ServiceUsageAsyncClient()
    service_name = "compute.googleapis.com"
    # NOTE: The compute API must be enabled before we can create a default network
    response = await service_usage_client.enable_service(
        request=service_usage_v1.EnableServiceRequest(
            name=f"projects/{gcp_project_id}/services/{service_name}"
        )
    )
    await response.result()

    compute_client = compute_v1.NetworksClient()
    default_network_exists = False
    for network in compute_client.list(project=gcp_project_id):
        if network.name == "default":
            default_network_exists = True
            break
    if not default_network_exists:
        request = compute_v1.InsertNetworkRequest(
            project=gcp_project_id,
            network_resource=compute_v1.Network(
                name="default",
                auto_create_subnetworks=True,
            ),
        )
        operation = compute_client.insert(request=request)
        operation.result()


async def _create_gcp_service_account(gcp_project_id: str):
    try:
        import googleapiclient.discovery
    except ImportError:
        raise exceptions.MissingGCPDependency()

    iam_service = googleapiclient.discovery.build("iam", "v1")
    _ = (
        iam_service.projects()
        .serviceAccounts()
        .create(
            name=f"projects/{gcp_project_id}",
            body={"accountId": "launchflow"},
        )
        .execute()
    )
    # NOTE: we "manually" construct the email otherwise gcp will stick the project ID number
    # in it which doesn't look as nice.
    return f"launchflow@{gcp_project_id}.iam.gserviceaccount.com"


async def _create_gcs_artifact_bucket(
    launchflow_project_name: str, launchflow_environment_name: str, gcp_project_id: str
):
    try:
        from google.api_core.exceptions import Conflict
        from google.cloud import storage
    except ImportError:
        raise exceptions.MissingGCPDependency()

    storage_client = storage.Client(project=gcp_project_id)
    bucket_name = f"{launchflow_project_name}-{launchflow_environment_name}-artifacts"
    for unique_bucket_name in unique_resource_name_generator(bucket_name):
        try:
            bucket = storage_client.create_bucket(unique_bucket_name)
            break
        except Conflict:
            continue
    bucket.add_lifecycle_delete_rule(
        # TODO: consider making this configurable
        age=14,
        matches_prefix=["logs"],
    )
    bucket.patch()
    return bucket.name


async def check_vpc_service_connection(gcp_project_id: str):
    try:
        import googleapiclient.discovery
        from googleapiclient import errors
    except ImportError:
        raise exceptions.MissingGCPDependency()

    services_service = googleapiclient.discovery.build("servicenetworking", "v1")
    try:
        connections = (
            services_service.services()
            .connections()
            .list(
                network=f"projects/{gcp_project_id}/global/networks/default",
                parent="services/servicenetworking.googleapis.com",
            )
            .execute()
        )
        # If no connections are returned we need to enable VPC peering
        return not (bool(connections))
    except errors.HttpError:
        # If an error occurred just attempt to enable VPC peering
        # This can happen if the project does not have the Service Networking API enabled
        # which will be enabled by the tofu apply
        return True


async def create_gcp_environment(
    inputs: GCPEnvironmentCreationInputs,
) -> GCPEnvironmentCreationOutputs:
    # NOTE: we do this before so all prompts are done before we start the progress bar
    if not inputs.gcp_project_id:
        org_name = await lookup_organization()
        billing_accound_name = await lookup_billing_account()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("["),
        TimeElapsedColumn(),
        TextColumn("]"),
    ) as progress:
        artifact_bucket = None
        gcp_project_id = None
        service_account_email = None
        try:
            if inputs.gcp_project_id:
                gcp_project_id = inputs.gcp_project_id
            else:
                create_project_task = progress.add_task(
                    "Creating GCP project...", total=1
                )
                gcp_project_id = await _create_gcp_project(
                    project_name=inputs.launchflow_project_name,
                    environment_name=inputs.launchflow_environment_name,
                    org_name=org_name,
                )
                await _assign_billing_project(gcp_project_id, billing_accound_name)
                await _maybe_create_default_network(gcp_project_id)
                progress.console.print(
                    f"[green]✓ GCP Project: `{gcp_project_id}` successfully created[/green]"
                )
                progress.remove_task(create_project_task)
            # TODO: bucket and sa can be created in parallel
            if inputs.environment_service_account_email:
                service_account_email = inputs.environment_service_account_email
            else:
                create_sa = progress.add_task(
                    "Creating environment service account...", total=1
                )
                service_account_email = await _create_gcp_service_account(
                    gcp_project_id
                )
                progress.console.print(
                    f"[green]✓ Environment service account: `{service_account_email}` successfully created[/green]"
                )
                progress.remove_task(create_sa)
            if inputs.artifact_bucket:
                artifact_bucket = inputs.artifact_bucket
            else:
                create_bucket = progress.add_task(
                    "Creating artifact bucket...", total=1
                )
                artifact_bucket = await _create_gcs_artifact_bucket(
                    launchflow_project_name=inputs.launchflow_project_name,
                    launchflow_environment_name=inputs.launchflow_environment_name,
                    gcp_project_id=gcp_project_id,
                )
                progress.console.print(
                    f"[green]✓ Artifact bucket: `{artifact_bucket}` successfully created[/green]"
                )
                progress.remove_task(create_bucket)
            enable_vpc_connection = True
            if inputs.gcp_project_id:
                enable_vpc_connection = await check_vpc_service_connection(
                    gcp_project_id
                )

            if isinstance(config.launchflow_yaml.backend, LocalBackend):
                state_prefix = f"{config.launchflow_yaml.backend.path}/{inputs.launchflow_environment_name}"
            elif isinstance(config.launchflow_yaml.backend, GCSBackend):
                state_prefix = f"{config.launchflow_yaml.backend.prefix}/{inputs.launchflow_environment_name}"
            elif isinstance(config.launchflow_yaml.backend, LaunchFlowBackend):
                state_prefix = f"{inputs.launchflow_project_name}/environments/{inputs.launchflow_environment_name}/tofu-state?lock_id={inputs.lock_id}"

            else:
                raise ValueError("Only local backend is supported")

            command = TFApplyCommand(
                tf_module_dir="workflows/tf/environments/gcp",
                backend=config.launchflow_yaml.backend,
                tf_state_prefix=state_prefix,
                tf_vars={
                    "gcp_project_id": gcp_project_id,
                    "environment_service_account_email": service_account_email,
                    "enable_vpc_connection": str(enable_vpc_connection).lower(),
                },
            )
            await run_tofu(command)
            progress.console.print(
                f"[green]✓ GCP project: `{gcp_project_id}` is fully configured[/green]"
            )
        except Exception:
            logging.exception("Failed to create GCP environment")
            for task in progress.tasks:
                progress.remove_task(task.id)
            return GCPEnvironmentCreationOutputs(
                artifact_bucket=artifact_bucket,
                environment_service_account_email=service_account_email,
                gcp_project_id=gcp_project_id,
                success=False,
            )
        return GCPEnvironmentCreationOutputs(
            artifact_bucket=artifact_bucket,
            environment_service_account_email=service_account_email,
            gcp_project_id=gcp_project_id,
            success=True,
        )
