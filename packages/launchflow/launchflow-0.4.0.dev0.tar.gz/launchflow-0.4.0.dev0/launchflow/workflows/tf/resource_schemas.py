import enum
from typing import Dict, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class PostgresVersion(enum.Enum):
    POSTGRES_15 = "POSTGRES_15"
    POSTGRES_14 = "POSTGRES_14"
    POSTGRES_13 = "POSTGRES_13"
    POSTGRES_12 = "POSTGRES_12"
    POSTGRES_11 = "POSTGRES_11"
    POSTGRES_10 = "POSTGRES_10"
    POSTGRES_9_6 = "POSTGRES_9_6"


class CreateGcpSqlPostgresRequest(BaseModel):
    postgres_version: PostgresVersion


class CreateGcpSecretManagerSecret(BaseModel):
    pass


class CreateGcpPubsubTopicRequest(BaseModel):
    pass


class CreateGcpStorageBucketRequest(BaseModel):
    location: str


class CreateGcpBigQueryDatasetRequest(BaseModel):
    location: str


class CreateGcpMemorystoreRedisRequest(BaseModel):
    memory_size_gb: int = 1


class CreateGcpComputeEngineRedisRequest(BaseModel):
    pass


class DockerConfig(BaseModel):
    image: str
    args: List[str]
    environment_variables: Dict[str, str]


class FirewallConfig(BaseModel):
    expose_ports: List[int]


class CreateGcpComputeEngineRequest(BaseModel):
    additional_outputs: Dict[str, str]
    docker_cfg: DockerConfig
    firewall_cfg: Optional[FirewallConfig] = None


class CreateAwsS3BucketRequest(BaseModel):
    # If this is none we fall back to what region the environment is configured in.
    region: Optional[str] = None


class CreateAwsSecretsManagerSecret(BaseModel):
    pass


class CreateAwsRdsPostgresRequest(BaseModel):
    pass


class CreateAwsElasticacheRedisRequest(BaseModel):
    pass


class CreateAwsEC2Request(BaseModel):
    additional_outputs: Dict[str, str]
    docker_cfg: DockerConfig
    firewall_cfg: Optional[FirewallConfig] = None
