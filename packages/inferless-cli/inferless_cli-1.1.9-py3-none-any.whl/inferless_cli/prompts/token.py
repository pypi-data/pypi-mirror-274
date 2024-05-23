import typer
from typing_extensions import Optional
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from inferless_cli.utils.helpers import (
    get_by_keys,
    save_cli_tokens,
    save_tokens,
)
from inferless_cli.utils.services import get_workspaces_list, validate_cli_token

app = typer.Typer(
    no_args_is_help=True,
)


@app.command(
    "set",
    help="Set account credentials for connecting to Inferless. If not provided with the command, you will be prompted to enter your credentials.",
)
def set_token(
    token_key: Optional[str] = typer.Option(help="Account CLI key"),
    token_secret: Optional[str] = typer.Option(help="Account CLI secret"),
):
    if token_key is None:
        token_key = prompt("CLI key:", is_password=True)
    if token_secret is None:
        token_secret = prompt("CLI secret:", is_password=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description="Verifying credentials...", total=None)
        if token_key and token_secret:
            try:
                details = validate_cli_token(token_key, token_secret)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            # Check the response
            if not details["access"] and not details["refresh"] and not details["user"]:
                progress.update(
                    task_id,
                    description="Credentials couldn't be verified. Please try again",
                )
                progress.remove_task(task_id)
                rich.print(
                    "[red]Credentials couldn't be verified. Please try again[/red]"
                )
                raise typer.Abort()
            else:
                progress.update(task_id, description="Credentials verified!")
                progress.remove_task(task_id)
                rich.print("[green]Credentials verified successfully![/green]")
                save_cli_tokens(token_key, token_secret)
                workspace_name = ""
                workspace_id = ""
                save_tokens(
                    details["access"],
                    details["refresh"],
                    details["user"]["id"],
                    workspace_id,
                    workspace_name,
                )
                workspaces = []
                # with Progress(
                #     SpinnerColumn(),
                #     TextColumn("[progress.description]{task.description}"),
                #     transient=True,
                # ) as progress:
                task = progress.add_task(description="fetching...", total=None)
                try:
                    workspaces = get_workspaces_list()
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)

                progress.remove_task(task)

                if (
                    "last_state" in details["user"]
                    and "last_workspace" in details["user"]["last_state"]
                ):
                    workspace_id = details["user"]["last_state"]["last_workspace"]
                    workspace_name = get_by_keys(
                        workspaces,
                        details["user"]["last_state"]["last_workspace"],
                        "id",
                        "name",
                    )
                else:
                    # select the 0th index of workspaces
                    workspace_id = workspaces[0].get("id")
                    workspace_name = workspaces[0].get("name")

                save_tokens(
                    details["access"],
                    details["refresh"],
                    details["user"]["id"],
                    workspace_id,
                    workspace_name,
                )
                rich.print("[green]Authentication finished successfully![/green]")
                rich.print(
                    f"[green]Token is connected to the [white]{workspace_name}[/white] workspace.[/green]"
                )


if __name__ == "__main__":
    app()
