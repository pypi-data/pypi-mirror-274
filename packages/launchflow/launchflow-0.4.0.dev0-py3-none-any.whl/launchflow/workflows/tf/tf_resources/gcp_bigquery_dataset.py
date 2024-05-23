import dataclasses

from launch_app.core.tf.tf import GCPTF
from launch_app.schemas.resource_schemas import CreateGcpBigQueryDatasetRequest


@dataclasses.dataclass
class GCPBigQueryDatasetTF(GCPTF[CreateGcpBigQueryDatasetRequest]):
    allow_nonempty_delete: bool

    @classmethod
    def production(cls, **kwargs):
        kwargs = {"allow_nonempty_delete": False, **kwargs}
        return cls(**kwargs)

    @classmethod
    def development(cls, **kwargs):
        kwargs = {"allow_nonempty_delete": True, **kwargs}
        return cls(**kwargs)

    def tf_cwd(self):
        return "tf/resources/gcp_bigquery_dataset"

    def tf_vars(self):
        return {
            "gcp_project_id": self.gcp_project_id,
            "gcp_region": self.gcp_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "location": self.create_request.location,
            "allow_nonempty_delete": str(self.allow_nonempty_delete).lower(),
        }
