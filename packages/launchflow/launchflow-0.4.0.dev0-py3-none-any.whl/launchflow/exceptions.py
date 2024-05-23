from typing import Optional

from launchflow.utils import get_failure_text


class LaunchFlowException(Exception):
    def pretty_print(self):
        print(self)


class LaunchFlowRequestFailure(LaunchFlowException):
    def __init__(self, response) -> None:
        super().__init__(get_failure_text(response))
        self.status_code = response.status_code


class LaunchFlowOperationFailure(LaunchFlowException):
    def __init__(self, status_message: str) -> None:
        super().__init__(status_message)


# TODO: Move "potential fix" messsages into the server.
# Server should return a json payload with a message per client type, i.e.
# {status: 409, message: "Conflict...", fix: {"cli": "Run this command..."}}
# Use details to return the fix payload:
# details = {message: "...", fix: {"cli": "Run this command..."}}
class ConnectionInfoNotFound(Exception):
    def __init__(self, resource_name: str) -> None:
        super().__init__(
            f"Connection info for resource '{resource_name}' not found. "
            f"\n\nPotential Fix:\nRun `launchflow create` it.\n\n"
        )


class PermissionCannotReadConnectionInfo(Exception):
    def __init__(self, resource_name: str, connection_path: str) -> None:
        super().__init__(
            f"Permission denied reading connection info for resource '{resource_name}' please ensure you have access to read the bucket: {connection_path}"
        )


class ForbiddenConnectionInfo(Exception):
    def __init__(self, bucket_url) -> None:
        super().__init__(
            f"Failed to read connection info from bucket. Please ensure you have access at: {bucket_url}"
        )


class ProjectOrEnvironmentNotSet(Exception):
    def __init__(self, project: Optional[str], environment: Optional[str]) -> None:
        super().__init__(
            f"Project or environment name not set. Set the project and environment names using "
            f"launchflow.yaml or the environment variables LAUNCHFLOW_PROJECT and LAUNCHFLOW_ENVIRONMENT. "
            f"\n\nCurrent project: {project}\nCurrent environment: {environment}\n\n"
        )


class RemoteConnectionInfoMissing(Exception):
    def __init__(self, remote_resource_info) -> None:
        super().__init__(
            f"Remote connection info for resource '{remote_resource_info}' is missing. "
            f"\n\nPotential Fix:\nRun `launchflow create` to create the resource or "
            f"`launchflow connect` to connect to it.\n\n"
        )


class OperationNotStarted(Exception):
    def __init__(self, operation: str) -> None:
        super().__init__(f"Operation '{operation}' not started. ")


class OperationAlreadyStarted(Exception):
    def __init__(self, operation: str) -> None:
        super().__init__(
            f"Operation '{operation}' already started. "
            f"\n\nPotential Fix:\nRun `launchflow start` to start the operation.\n\n"
        )


class ResourceReplacementRequired(Exception):
    def __init__(self, resource_name: str) -> None:
        super().__init__(
            f"Resource '{resource_name}' already exists but the create operation "
            "requires replacement, which must be explicitly specified. "
        )


class ResourceProductMismatch(Exception):
    def __init__(self, product: str, resource: str) -> None:
        super().__init__(
            f"Product '{product}' does not match the product of resource '{resource}'."
        )


class ServiceProductMismatch(Exception):
    def __init__(self, product: str, service: str) -> None:
        super().__init__(
            f"Product '{product}' does not match the product of service '{service}'."
        )


class GCPConfigNotFound(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"GCP configuration not found for environment '{environment_name}'. "
            "This environment is most likely an AWS environment."
        )


class EnvironmentNotFound(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' not found. Create the environment with `launchflow environments create {environment_name}`."
        )


class LaunchFlowProjectNotFound(Exception):
    def __init__(self, project_name: str) -> None:
        super().__init__(
            f"LaunchFlow project '{project_name}' not found. Create the project with `launchflow projects create {project_name}`."
        )


class LaunchFlowEnvironmentNotFound(EnvironmentNotFound):
    def __init__(self, project_name: str, environment_name: str) -> None:
        super().__init__(
            f"LaunchFlow environment '{project_name}/{environment_name}' not found. Create the project with `launchflow environments create {environment_name}`."
        )


class LaunchFlowResourceNotFound(Exception):
    def __init__(
        self, project_name: str, environment_name: str, resource_name: str
    ) -> None:
        super().__init__(
            f"LaunchFlow resource '{project_name}/{environment_name}/{resource_name}' not found."
        )


class ServiceNotFound(Exception):
    def __init__(self, service_name: str) -> None:
        super().__init__(f"Service '{service_name}' not found.")


class ResourceNotFound(Exception):
    def __init__(self, resource_name: str) -> None:
        super().__init__(f"Resource '{resource_name}' not found.")


class MultipleBillingAccounts(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You have access to multiple billing accounts. This is currently not supported.",
        )


class NoBillingAccountAccess:
    def __init__(self) -> None:
        super().__init__(
            "You do not have access to a billing account. Ensure you have access to a billing account and try again.",
        )


class MultipleOrgs(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You have access to multiple organizations. This is currently not supported.",
        )


class NoOrgs(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You do not have access to any organizations. Ensure you have access to an organiztaion and try again."
        )


class TofuOutputFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu output failed")


class TofuApplyFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu apply failed")


class TofuInitFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu init failed")


class TofuImportFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu import failed")


class TofuDestroyFailure(Exception):
    def __init__(self) -> None:
        super().__init__("Tofu destroy failed")


class EntityLocked(Exception):
    def __init__(self, entity: str) -> None:
        super().__init__(
            f"Entity is locked (`{entity}`). Wait for the operation to complete."
        )


class LockMismatch(Exception):
    def __init__(self, entity: str) -> None:
        super().__init__(
            f"Cannot unlock an entity (`{entity}`) that you do not hold the lock for."
        )


class MissingGCPDependency(Exception):
    def __init__(self) -> None:
        super().__init__(
            "GCP dependencies are not installed. Install them with: `pip install launchflow[gcp]`"
        )


class MissingAWSDependency(Exception):
    def __init__(self) -> None:
        super().__init__(
            "AWS dependencies are not installed. Install them with: `pip install launchflow[aws]`"
        )


class LaunchFlowYamlNotFound(Exception):
    def __init__(self) -> None:
        super().__init__(
            "No launchflow.yaml could be found, please ensure you are in the correct directory."
        )


# TODO: Add a link to documentation for setting up AWS credentials.
class NoAWSCredentialsFound(Exception):
    def __init__(self) -> None:
        super().__init__(
            "No AWS credentials found. Please ensure you have AWS credentials set up in your environment."
        )


class ExistingEnvironmentDifferentEnvironmentType(Exception):
    def __init__(self, environment_name: str, environment_type: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' already exists with a different environment type '{environment_type}'."
        )


class ExistingEnvironmentDifferentCloudProvider(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(
            f"Environment '{environment_name}' already exists with a different cloud provider type."
        )


class FailedToDeleteEnvironment(Exception):
    def __init__(self, environment_name: str) -> None:
        super().__init__(f"Failed to delete environment '{environment_name}'.")


class GCSObjectNotFound(Exception):
    def __init__(self, bucket: str, prefix: str) -> None:
        super().__init__(
            f"GCS object not found in bucket '{bucket}' with prefix '{prefix}'."
        )


class FlowStateNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Flow state not found.")


class OpenTofuInstallFailure(Exception):
    def __init__(self) -> None:
        super().__init__("OpenTofu install failed.")
