import dataclasses

from launch_app.core.tf.tf import AWSTF, LaunchflowURI
from launch_app.schemas.resource_schemas import CreateAwsElasticacheRedisRequest


@dataclasses.dataclass
class AWSElasticacheRedisTF(AWSTF[CreateAwsElasticacheRedisRequest]):
    node_type: str
    parameter_group_name: str
    engine_version: str

    @classmethod
    def production(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateAwsElasticacheRedisRequest,
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
            node_type="cache.r7g.large",
            parameter_group_name="default.redis7",
            engine_version="7.0",
        )

    @classmethod
    def development(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateAwsElasticacheRedisRequest,
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
            node_type="cache.t4g.micro",
            parameter_group_name="default.redis7",
            engine_version="7.0",
        )

    def tf_cwd(self):
        return "tf/resources/aws_elasticache_redis"

    def tf_vars(self):
        return {
            "aws_region": self.aws_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "launchflow_project": self.launchflow_uri.project_name,
            "launchflow_environment": self.launchflow_uri.environment_name,
            "vpc_id": self.vpc_id,
            "node_type": self.node_type,
            "parameter_group_name": self.parameter_group_name,
            "engine_version": self.engine_version,
        }
