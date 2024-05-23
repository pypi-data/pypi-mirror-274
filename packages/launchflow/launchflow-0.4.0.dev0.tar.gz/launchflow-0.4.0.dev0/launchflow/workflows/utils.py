import random
import tempfile
from typing import Generator, Optional

from launchflow.workflows.commands.tf_commands import TFCommand


# NOTE: The first time this generator is called, it will yield the base_name. Every
# time after that, it will yield the base_name with a random number appended to it.
def unique_resource_name_generator(
    base_name: str, join_str: str = "-", max_length: Optional[int] = None
) -> Generator[str, None, None]:
    rand_value = None
    if max_length is not None and len(base_name) > max_length:
        base_name = base_name[:max_length]
    while True:
        if rand_value is None:
            yield base_name
        else:
            # NOTE: the default join_str is a dash, so the default output will be
            # something like "my-resource-1234"
            random_addition = f"{join_str}{rand_value}"
            if max_length is not None:
                # NOTE: if the max_length is set, we need to make sure the random
                # addition doesn't exceed it
                if len(base_name) + len(random_addition) > max_length:
                    base_name = base_name[: max_length - len(random_addition)]
            yield f"{base_name}{random_addition}"

            yield f"{base_name}{join_str}{rand_value}"
        rand_value = random.randint(1000, 9999)


async def run_tofu(command: TFCommand):
    with tempfile.TemporaryDirectory() as tempdir:
        return await command.run(tempdir)
