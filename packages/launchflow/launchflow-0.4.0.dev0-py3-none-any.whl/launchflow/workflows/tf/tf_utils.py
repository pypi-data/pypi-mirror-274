from typing import Any

from launchflow.models.flow_state import Environment as FlowStateEnvironment
from launchflow.models.flow_state import Resource as FlowStateResource
from launchflow.workflows.tf.tf import GCPTF, TF
from launchflow.workflows.tf.tf_resources.gcp_storage_bucket import GCPStorageBucketTF

PRODUCT_NAME_TO_TF_CLASS = {
    "gcp_storage_bucket": GCPStorageBucketTF,
}


# TODO If we store the environment type, return the dev/prod TF
def resource_to_tf(resource: Any, environment: FlowStateEnvironment) -> TF:
    if resource.product_name not in PRODUCT_NAME_TO_TF_CLASS:
        raise ValueError(f"Product name {resource.product_name} wasn't mapped to a TF class.")

    tf_class = PRODUCT_NAME_TO_TF_CLASS[resource.product_name]

    if environment.gcp_config is None:
        raise NotImplementedError

    if issubclass(tf_class, GCPTF):
        return tf_class(
            gcp_project_id=environment.gcp_config.project_id,
            gcp_region=environment.gcp_config.default_region,
            artifact_bucket=environment.gcp_config.artifact_bucket,
            resource_name=resource.name,
            create_args=resource._create_args
        )

    raise NotImplementedError


def flowstate_resource_to_tf(resource: FlowStateResource, environment: FlowStateEnvironment) -> TF:
    if (product_name := resource.product.name.lower()) not in PRODUCT_NAME_TO_TF_CLASS:
        raise ValueError(f"Product name {product_name} wasn't mapped to a TF class.")

    tf_class = PRODUCT_NAME_TO_TF_CLASS[product_name]

    if environment.gcp_config is None:
        raise NotImplementedError

    if issubclass(tf_class, GCPTF):
        return tf_class(
            gcp_project_id=environment.gcp_config.project_id,
            gcp_region=environment.gcp_config.default_region,
            artifact_bucket=environment.gcp_config.artifact_bucket,
            resource_name=resource.name,
            create_args=resource.create_args
        )

    raise NotImplementedError
