import httpx
import rich
import typer

from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.clients import async_launchflow_client_ctx
from launchflow.clients.projects_client import ProjectsAsyncClient
from launchflow.config import config
from launchflow.exceptions import LaunchFlowException
from launchflow.flows.project_flows import create_project

app = UTyper(help="Interact with your LaunchFlow projects.")


@app.command()
async def list(
    launch_url: str = typer.Option(
        "https://launch.launchflow.com", help="The LaunchFlow URL.", hidden=True
    )
):
    """Lists all current projects in your account."""

    async with httpx.AsyncClient(timeout=60) as client:
        proj_client = ProjectsAsyncClient(http_client=client, base_url=launch_url)
        projects = await proj_client.list(config.settings.default_account_id)
    print_response(
        "Projects",
        {
            "projects": [
                projects.model_dump(exclude_defaults=True) for projects in projects
            ]
        },
    )


@app.command()
async def get(
    project_name: str,
    launch_url: str = typer.Option(
        "https://launch.launchflow.com", help="The LaunchFlow URL.", hidden=True
    ),
):
    """Get information about a specific project."""
    async with httpx.AsyncClient(timeout=60) as client:
        proj_client = ProjectsAsyncClient(http_client=client, base_url=launch_url)
        project = await proj_client.get(project_name)
    print_response("Project", project.model_dump(exclude_defaults=True))


@app.command()
async def create(
    project_name: str = typer.Argument(None, help="The name of the project to create."),
    account_id: str = typer.Option(
        None,
        help="The account ID to fetch. Of the format `acount_123`. Defaults to the account in your config file.",  # noqa: E501
    ),
):
    """Create a new project in your account."""
    async with async_launchflow_client_ctx() as client:
        try:
            project = await create_project(
                client=client, project_name=project_name, account_id=account_id
            )
        except LaunchFlowException:
            raise typer.Exit(1)

    print_response("Project", project.model_dump(exclude_defaults=True))


@app.command()
async def delete(name: str = typer.Argument(..., help="The project name.")):
    """Delete a project."""
    try:
        async with async_launchflow_client_ctx() as client:
            await client.projects.delete(name)

    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    rich.print("[green]✓[/green] Project deleted.")
