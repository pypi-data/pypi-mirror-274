import re

MAX_ENVIRONMENT_NAME_LENGTH = 15
MIN_ENVIRONMENT_NAME_LENGTH = 1
ENVIRONMENT_PATTERN = "^[a-z0-9-]+$"
RESERVED_ENVIRONMENT_NAMES = {
    "gcp",
    "aws",
    "azure",
    "local",
    "base",
    "default",
    "nix",
}


def validate_environment_name(environment_name: str):
    if len(environment_name) > MAX_ENVIRONMENT_NAME_LENGTH:
        raise ValueError(
            f"Environment name must be at most {MAX_ENVIRONMENT_NAME_LENGTH} characters long"
        )
    if len(environment_name) < MIN_ENVIRONMENT_NAME_LENGTH:
        raise ValueError(
            f"Environment name must be at least {MIN_ENVIRONMENT_NAME_LENGTH} characters long"
        )
    if not re.match(ENVIRONMENT_PATTERN, environment_name):
        raise ValueError(f"Environment name must match pattern {ENVIRONMENT_PATTERN}")

    if environment_name in RESERVED_ENVIRONMENT_NAMES:
        raise ValueError(f"Environment name is reserved: {environment_name}")
