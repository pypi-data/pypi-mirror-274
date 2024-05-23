import dataclasses

from launch_app.core.tf.tf import GCPTF
from launch_app.schemas.resource_schemas import CreateGcpStorageBucketRequest


@dataclasses.dataclass
class GCPSecretManagerSecretTF(GCPTF[CreateGcpStorageBucketRequest]):
    @classmethod
    def production(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def development(cls, **kwargs):
        return cls(**kwargs)

    def tf_cwd(self):
        return "tf/resources/gcp_secret_manager"

    def tf_vars(self):
        return {
            "gcp_project_id": self.gcp_project_id,
            "gcp_region": self.gcp_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
        }
