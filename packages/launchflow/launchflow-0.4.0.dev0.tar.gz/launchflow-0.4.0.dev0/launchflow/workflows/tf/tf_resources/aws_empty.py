import dataclasses

from launch_app.core.tf.tf import AWSTF


@dataclasses.dataclass
class AWSEmptyResourceTF(AWSTF[None]):
    @classmethod
    def production(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def development(cls, **kwargs):
        return cls(**kwargs)

    def tf_cwd(self):
        return "tf/empty/aws_empty"

    def tf_vars(self):
        return {
            "region": self.aws_region,
        }
