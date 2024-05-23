import dataclasses

from launchflow.workflows.tf.resource_schemas import CreateGcpStorageBucketRequest
from launchflow.workflows.tf.tf import GCPTF


@dataclasses.dataclass
class GCPStorageBucketTF(GCPTF[CreateGcpStorageBucketRequest]):
    @classmethod
    def production(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def development(cls, **kwargs):
        return cls(**kwargs)

    def tf_cwd(self):
        return "workflows/tf/resources/gcp_storage_bucket"

    def tf_vars(self):
        return {
            "gcp_project_id": self.gcp_project_id,
            "resource_name": self.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "gcp_region": self.create_args["location"],
        }
