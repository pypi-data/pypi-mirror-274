import dataclasses

from launch_app.core.tf.tf import GCPTF


@dataclasses.dataclass
class GCPEmptyResourceTF(GCPTF[None]):
    @classmethod
    def production(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def development(cls, **kwargs):
        return cls(**kwargs)

    def tf_cwd(self):
        return "tf/empty/gcp_empty"

    def tf_vars(self):
        return {}
