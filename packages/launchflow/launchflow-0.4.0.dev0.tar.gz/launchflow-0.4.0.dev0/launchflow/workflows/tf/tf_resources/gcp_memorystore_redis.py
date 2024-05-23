import dataclasses

from launch_app.core.tf.tf import GCPTF, LaunchflowURI
from launch_app.schemas.resource_schemas import CreateGcpMemorystoreRedisRequest


@dataclasses.dataclass
class GCPMemorystoreRedisTF(GCPTF[CreateGcpMemorystoreRedisRequest]):
    redis_tier: str
    memory_size_gb: int

    @classmethod
    def production(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateGcpMemorystoreRedisRequest,
        # GCPTF fields
        gcp_project_id: str,
        gcp_region: str,
        admin_service_account_email: str,
        env_service_account_email: str,
    ):
        return cls(
            gcs_backend_bucket=gcs_backend_bucket,
            artifact_bucket=artifact_bucket,
            launchflow_uri=launchflow_uri,
            create_request=create_request,
            gcp_project_id=gcp_project_id,
            gcp_region=gcp_region,
            admin_service_account_email=admin_service_account_email,
            env_service_account_email=env_service_account_email,
            # Fields from create_request
            memory_size_gb=create_request.memory_size_gb,
            # Prod-type Environment fields below
            redis_tier="STANDARD_HA",
        )

    @classmethod
    def development(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateGcpMemorystoreRedisRequest,
        # GCPTF fields
        gcp_project_id: str,
        gcp_region: str,
        admin_service_account_email: str,
        env_service_account_email: str,
    ):
        return cls(
            gcs_backend_bucket=gcs_backend_bucket,
            artifact_bucket=artifact_bucket,
            launchflow_uri=launchflow_uri,
            create_request=create_request,
            gcp_project_id=gcp_project_id,
            gcp_region=gcp_region,
            admin_service_account_email=admin_service_account_email,
            env_service_account_email=env_service_account_email,
            # Fields from create_request
            memory_size_gb=create_request.memory_size_gb,
            # Prod-type Environment fields below
            redis_tier="BASIC",
        )

    def tf_cwd(self):
        return "tf/resources/gcp_memorystore_redis"

    def tf_vars(self):
        return {
            "gcp_project_id": self.gcp_project_id,
            "gcp_region": self.gcp_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "redis_tier": self.redis_tier,
            "memory_size_gb": self.memory_size_gb,
        }
