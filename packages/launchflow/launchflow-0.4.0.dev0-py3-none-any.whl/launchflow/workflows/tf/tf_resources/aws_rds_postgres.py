import dataclasses

from launch_app.core.tf.tf import AWSTF, LaunchflowURI
from launch_app.schemas.resource_schemas import CreateAwsRdsPostgresRequest


# NOTE: AWS RDS only supports alphanumeric characters.
def _convert_resource_name_to_camel_case(s: str) -> str:
    # Split the string by both dashes and underscores, then capitalize each word
    # Finally, join them together without any separators to form CamelCase
    return "".join(word.capitalize() for word in s.replace("-", "_").split("_"))


@dataclasses.dataclass
class AWSRDSPostgresTF(AWSTF[CreateAwsRdsPostgresRequest]):
    publicly_accessible: bool
    instance_count: int
    instance_class: str

    @classmethod
    def production(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateAwsRdsPostgresRequest,
        # AWSTF fields
        aws_region: str,
        vpc_id: str,
        aws_account_id: str,
        aws_external_role_id: str,
        aws_iam_role_arn: str,
    ):
        return cls(
            gcs_backend_bucket=gcs_backend_bucket,
            artifact_bucket=artifact_bucket,
            launchflow_uri=launchflow_uri,
            create_request=create_request,
            aws_region=aws_region,
            vpc_id=vpc_id,
            aws_account_id=aws_account_id,
            aws_external_role_id=aws_external_role_id,
            aws_iam_role_arn=aws_iam_role_arn,
            # Prod-type Environment fields below
            publicly_accessible=False,
            instance_count=2,
            instance_class="db.r5.large",
        )

    @classmethod
    def development(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateAwsRdsPostgresRequest,
        # AWSTF fields
        aws_region: str,
        vpc_id: str,
        aws_account_id: str,
        aws_external_role_id: str,
        aws_iam_role_arn: str,
    ):
        return cls(
            gcs_backend_bucket=gcs_backend_bucket,
            artifact_bucket=artifact_bucket,
            launchflow_uri=launchflow_uri,
            create_request=create_request,
            aws_region=aws_region,
            vpc_id=vpc_id,
            aws_account_id=aws_account_id,
            aws_external_role_id=aws_external_role_id,
            aws_iam_role_arn=aws_iam_role_arn,
            # Dev-type Environment fields below
            publicly_accessible=True,
            instance_count=1,
            instance_class="db.t4g.medium",
        )

    def tf_cwd(self):
        return "tf/resources/aws_rds_postgres"

    def tf_vars(self):
        return {
            "aws_region": self.aws_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "launchflow_project": self.launchflow_uri.project_name,
            "launchflow_environment": self.launchflow_uri.environment_name,
            "vpc_id": self.vpc_id,
            "database_name": _convert_resource_name_to_camel_case(
                self.launchflow_uri.resource_name
            ),
            "publicly_accessible": str(self.publicly_accessible).lower(),
            "instance_count": self.instance_count,
            "instance_class": self.instance_class,
        }
