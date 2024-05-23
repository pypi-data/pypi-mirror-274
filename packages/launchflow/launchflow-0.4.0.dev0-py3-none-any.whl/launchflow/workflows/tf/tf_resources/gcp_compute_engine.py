import dataclasses
import json
from typing import Any, Dict, List

from launch_app.core.tf.tf import GCPTF
from launch_app.schemas.resource_schemas import CreateGcpComputeEngineRequest


@dataclasses.dataclass
class GCPComputeEngineTF(GCPTF[CreateGcpComputeEngineRequest]):
    machine_type: str

    @classmethod
    def production(cls, **kwargs):
        return cls(**kwargs, machine_type="n1-standard-1")

    @classmethod
    def development(cls, **kwargs):
        return cls(**kwargs, machine_type="f1-micro")

    def tf_cwd(self) -> str:
        return "tf/resources/gcp_compute_engine"

    def tf_vars(self) -> Dict[str, Any]:
        def format_environment_variables(environment_variables: Dict[str, str]) -> List[Dict[str, str]]:
            output = []

            for k, v in environment_variables.items():
                output.append({"name": k, "value": v})

            return output

        docker_image = self.create_request.docker_cfg.image
        docker_args = self.create_request.docker_cfg.args
        docker_environment_variables = format_environment_variables(self.create_request.docker_cfg.environment_variables)

        expose_ports = []
        if self.create_request.firewall_cfg is not None:
            expose_ports = self.create_request.firewall_cfg.expose_ports

        return {
            "gcp_project_id": self.gcp_project_id,
            "gcp_region": self.gcp_region,
            "artifact_bucket": self.artifact_bucket,
            "machine_type": self.machine_type,
            "resource_name": self.launchflow_uri.resource_name,
            "environment_service_account_email": self.env_service_account_email,

            # Non-nullable request input variables
            "additional_outputs": json.dumps(self.create_request.additional_outputs),
            "docker_image": docker_image,
            "docker_args": json.dumps(docker_args),
            "docker_environment_variables": json.dumps(docker_environment_variables),
            # Nullable request input variables
            "expose_ports": expose_ports,
        }
