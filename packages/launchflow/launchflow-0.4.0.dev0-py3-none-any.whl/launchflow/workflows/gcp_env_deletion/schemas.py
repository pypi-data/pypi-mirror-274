from dataclasses import dataclass

from launchflow.models.flow_state import Environment


@dataclass
class GCPEnvironmentDeletionInputs:
    launchflow_project_name: str
    launchflow_environment_name: str
    environment: Environment
