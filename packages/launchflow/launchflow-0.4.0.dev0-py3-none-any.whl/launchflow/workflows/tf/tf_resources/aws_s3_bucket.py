import dataclasses
from typing import Dict

from launch_app.core.tf.tf import AWSTF
from launch_app.schemas.resource_schemas import CreateAwsS3BucketRequest


@dataclasses.dataclass
class AWSS3BucketTF(AWSTF[CreateAwsS3BucketRequest]):
    @classmethod
    def production(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def development(cls, **kwargs):
        return cls(**kwargs)

    def tf_cwd(self) -> str:
        return "tf/resources/aws_s3_bucket"

    def tf_vars(self) -> Dict[str, str]:
        env_role_name = self.aws_iam_role_arn.split("/")[-1]
        return {
            "aws_region": self.aws_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "launchflow_project": self.launchflow_uri.project_name,
            "launchflow_environment": self.launchflow_uri.environment_name,
            "env_role_name": env_role_name,
        }
