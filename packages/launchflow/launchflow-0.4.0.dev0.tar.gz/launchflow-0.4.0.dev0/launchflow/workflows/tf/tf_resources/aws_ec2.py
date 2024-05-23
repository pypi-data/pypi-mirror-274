import dataclasses
import json
from typing import Any, Dict

from launch_app.core.tf.tf import AWSTF
from launch_app.schemas.resource_schemas import CreateAwsEC2Request


@dataclasses.dataclass
class AWSEC2TF(AWSTF[CreateAwsEC2Request]):
    machine_type: str

    @classmethod
    def production(cls, **kwargs):
        return cls(**kwargs, machine_type="t3.medium")

    @classmethod
    def development(cls, **kwargs):
        return cls(**kwargs, machine_type="t3.micro")

    def tf_cwd(self):
        return "tf/resources/aws_ec2"

    def tf_vars(self) -> Dict[str, Any]:
        docker_image = self.create_request.docker_cfg.image
        docker_args = self.create_request.docker_cfg.args
        docker_environment_variables = (
            self.create_request.docker_cfg.environment_variables
        )

        expose_ports = []
        if self.create_request.firewall_cfg is not None:
            expose_ports = self.create_request.firewall_cfg.expose_ports

        return {
            "aws_region": self.aws_region,
            "resource_name": self.launchflow_uri.resource_name,
            "artifact_bucket": self.artifact_bucket,
            "launchflow_project": self.launchflow_uri.project_name,
            "launchflow_environment": self.launchflow_uri.environment_name,
            "vpc_id": self.vpc_id,
            # Non-nullable request input variables
            "machine_type": self.machine_type,
            "additional_outputs": json.dumps(self.create_request.additional_outputs),
            "docker_image": docker_image,
            "docker_args": json.dumps(docker_args),
            "docker_environment_variables": json.dumps(docker_environment_variables),
            # Nullable request input variables
            "expose_ports": expose_ports,
        }
