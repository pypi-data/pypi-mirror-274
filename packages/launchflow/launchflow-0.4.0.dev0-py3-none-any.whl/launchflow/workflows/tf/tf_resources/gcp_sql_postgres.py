import dataclasses
from typing import Literal

from launch_app.core.tf.tf import GCPTF, LaunchflowURI
from launch_app.schemas.resource_schemas import CreateGcpSqlPostgresRequest


@dataclasses.dataclass
class GCPCloudSQLPostgresTF(GCPTF[CreateGcpSqlPostgresRequest]):
    postgres_db_version: str
    db_name: str
    user_name: str
    postgres_db_tier: str
    postgres_db_edition: str
    allow_public_access: bool
    availability_type: str = Literal["REGIONAL", "ZONAL"]
    deletion_protection: bool = True

    @classmethod
    def production(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateGcpSqlPostgresRequest,
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
            postgres_db_version=create_request.postgres_version.value,
            # Derived fields below
            db_name=f"{launchflow_uri.resource_name}-db",
            user_name=f"{launchflow_uri.resource_name}-user",
            # Prod-type Environment fields below
            postgres_db_tier="db-custom-1-3840",
            postgres_db_edition="ENTERPRISE",
            allow_public_access=False,
            availability_type="REGIONAL",
            deletion_protection=True,
        )

    @classmethod
    def development(
        cls,
        *,
        # TF fields
        gcs_backend_bucket: str,
        artifact_bucket: str,
        launchflow_uri: LaunchflowURI,
        create_request: CreateGcpSqlPostgresRequest,
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
            postgres_db_version=create_request.postgres_version.value,
            # Derived fields below
            db_name=f"{launchflow_uri.resource_name}-db",
            user_name=f"{launchflow_uri.resource_name}-user",
            # Dev-type Environment fields below
            postgres_db_tier="db-f1-micro",
            postgres_db_edition="ENTERPRISE",
            allow_public_access=True,
            availability_type="ZONAL",
            deletion_protection=False,
        )

    def tf_cwd(self):
        return "tf/resources/gcp_sql_postgres"

    def tf_vars(self):
        return {
            "gcp_project_id": self.gcp_project_id,
            "gcp_region": self.gcp_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "postgres_db_version": self.postgres_db_version,
            "db_name": self.db_name,
            "user_name": self.user_name,
            "postgres_db_tier": self.postgres_db_tier,
            "postgres_db_edition": self.postgres_db_edition,
            "allow_public_access": str(self.allow_public_access).lower(),
            "availability_type": self.availability_type,
            "deletion_protection": str(self.deletion_protection).lower(),
        }
