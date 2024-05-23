from enum import Enum


class StorageServiceProduct(str, Enum):
    # GCP product types
    GCP_CLOUD_RUN = "gcp_cloud_run"
    # AWS product types
    AWS_ECS_FARGATE = "aws_ecs_fargate"


class CloudProvider(str, Enum):
    GCP = "gcp"
    AWS = "aws"


class ResourceProduct(str, Enum):
    # GCP product types
    GCP_SQL_POSTGRES = "gcp_sql_postgres"
    GCP_PUBSUB_TOPIC = "gcp_pubsub_topic"
    GCP_PUBSUB_SUBSCRIPTION = "gcp_pubsub_subscription"
    GCP_STORAGE_BUCKET = "gcp_storage_bucket"
    GCP_BIGQUERY_DATASET = "gcp_bigquery_dataset"
    GCP_MEMORYSTORE_REDIS = "gcp_memorystore_redis"
    GCP_COMPUTE_ENGINE = "gcp_compute_engine"
    GCP_SECRET_MANAGER_SECRET = "gcp_secret_manager_secret"
    # AWS product types
    AWS_RDS_POSTGRES = "aws_rds_postgres"
    AWS_ELASTICACHE_REDIS = "aws_elasticache_redis"
    AWS_EC2 = "aws_ec2"
    AWS_SQS_QUEUE = "aws_sqs_queue"
    AWS_S3_BUCKET = "aws_s3_bucket"
    AWS_SECRETS_MANAGER_SECRET = "aws_secrets_manager_secret"


class ServiceProduct(str, Enum):
    # GCP product types
    GCP_CLOUD_RUN = "gcp_cloud_run"
    # AWS product types
    AWS_ECS_FARGATE = "aws_ecs_fargate"


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
