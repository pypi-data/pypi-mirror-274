import logging
from typing import Optional

import beaupy
import rich
import typer

from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.config import config
from launchflow.flows.environments_flows import create_environment, delete_environment
from launchflow.managers.environment_manager import EnvironmentManager
from launchflow.managers.flow_state_manager import FlowStateManager
from launchflow.models.enums import CloudProvider, EnvironmentType
from launchflow.validation import validate_environment_name

app = UTyper(help="Interact with your LaunchFlow environments.")


@app.command()
async def create(
    name: str = typer.Argument(None, help="The environment name."),
    env_type: Optional[EnvironmentType] = typer.Option(
        None, help="The environment type (`development` or `production`)."
    ),
    cloud_provider: Optional[CloudProvider] = typer.Option(
        None, help="The cloud provider."
    ),
):
    """Create a new environment in a LaunchFlow project."""
    if name is None:
        name = beaupy.prompt("Enter the environment name:")
        rich.print(f"[pink1]>[/pink1] {name}")
    validate_environment_name(name)
    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=name,
        backend=config.launchflow_yaml.backend,
    )
    try:
        environment = await create_environment(
            env_type,
            cloud_provider=cloud_provider,
            manager=environment_manager,
        )
    except Exception as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if environment is not None:
        print_response(
            "Environment",
            environment.model_dump(
                mode="json", exclude_defaults=True, exclude_none=True
            ),
        )


@app.command()
async def list():
    """List all environments in a LaunchFlow project."""
    manager = FlowStateManager(
        project_name=config.launchflow_yaml.project,
        backend=config.launchflow_yaml.backend,
    )
    try:
        envs = await manager.list_environments()
    except Exception as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    print_response(
        "Environments",
        {
            name: env.model_dump(mode="json", exclude_defaults=True, exclude_none=True)
            for name, env in envs.items()
        },
    )


@app.command()
async def get(
    name: str = typer.Argument(..., help="The environment name."),
):
    """Get information about a specific environment."""
    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=name,
        backend=config.launchflow_yaml.backend,
    )
    try:
        env = await environment_manager.load_environment()
    except Exception as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    print_response(
        "Environment",
        env.model_dump(mode="json", exclude_defaults=True, exclude_none=True),
    )


@app.command()
async def delete(
    name: str = typer.Argument(..., help="The environment name."),
    detach: bool = typer.Option(
        False,
        help="If true we will not clean up any of the cloud resources associated with the environment and will simply delete the record from LaunchFlow.",
    ),
):
    """Delete an environment."""
    if name is None:
        name = beaupy.prompt("Enter the environment name:")
        rich.print(f"[pink1]>[/pink1] {name}")
    environment_manager = EnvironmentManager(
        project_name=config.launchflow_yaml.project,
        environment_name=name,
        backend=config.launchflow_yaml.backend,
    )
    try:
        await delete_environment(detach=detach, manager=environment_manager)
    except Exception as e:
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    rich.print("[green]✓[/green] Environment deleted.")
