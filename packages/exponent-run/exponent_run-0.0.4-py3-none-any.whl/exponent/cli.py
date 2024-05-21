import asyncio
import logging
import os
import sys

import click
import httpx
from dotenv import load_dotenv

from exponent.core.config import get_settings, is_editable_install
from exponent.core.remote_execution.client import RemoteExecutionClient
from exponent.core.remote_execution.types import UseToolsConfig

load_dotenv()


@click.group()
def cli() -> None:
    """Exponent CLI group."""
    set_log_level()


@cli.command()
@click.option("--key", help="Your Exponent API Key")
@click.option(
    "--prod",
    is_flag=True,
    hidden=True,
    help="Use production URLs even if in editable mode",
)
def login(key: str, prod: bool) -> None:
    settings = get_settings(use_prod=prod)
    if is_editable_install() and not prod:
        click.secho(
            "Detected local editable install, using local URLs", fg="yellow", bold=True
        )
        click.secho("- base_url=", fg="yellow", bold=True, nl=False)
        click.secho(f"{settings.base_url}", fg=(100, 200, 255), bold=False)
        click.secho("- base_api_url=", fg="yellow", bold=True, nl=False)
        click.secho(f"{settings.base_api_url}", fg=(100, 200, 255), bold=False)
        click.secho()
    if not key:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/")
        return
    click.echo("Saving API Key to ~/.exponent...")
    if settings.api_key and settings.api_key != key:
        click.confirm("Detected existing API Key, continue? ", default=True, abort=True)
    with open(os.path.expanduser("~/.exponent"), "a") as f:
        f.write(f"\nEXPONENT_API_KEY={key}\n")
    click.echo("API Key saved.")


@cli.command()
@click.option(
    "--chat-id",
    help="ID of an existing chat session to reconnect",
    required=False,
)
@click.option(
    "--prod",
    is_flag=True,
    hidden=True,
    help="Use production URLs even if in editable mode",
)
@click.option(
    "--prompt",
    help="Start a chat with a given prompt.",
)
@click.option(
    "--benchmark",
    is_flag=True,
    help="Enable benchmarking mode",
)
def run(
    chat_id: str | None = None,
    prod: bool = False,
    prompt: str | None = None,
    benchmark: bool = False,
) -> None:
    chat_uuid = chat_id

    settings = get_settings(use_prod=prod)
    if is_editable_install() and not prod:
        click.secho(
            "Detected local editable install, using local URLs", fg="yellow", bold=True
        )
        click.secho("- base_url=", fg="yellow", bold=True, nl=False)
        click.secho(f"{settings.base_url}", fg=(100, 200, 255), bold=False)
        click.secho("- base_api_url=", fg="yellow", bold=True, nl=False)
        click.secho(f"{settings.base_api_url}", fg=(100, 200, 255), bold=False)
        click.secho()
    if not settings.api_key:
        click.echo("No API Key detected, redirecting to login...")
        click.launch(f"{settings.base_url}/")
        return
    else:
        api_key = settings.api_key

    loop = asyncio.get_event_loop()
    task = loop.create_task(
        start_client(
            api_key,
            settings.base_url,
            settings.base_api_url,
            chat_uuid=chat_uuid,
            prompt=prompt,
            benchmark=benchmark,
        )
    )
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass


async def start_client(  # noqa: PLR0913
    api_key: str,
    base_url: str,
    base_api_url: str,
    chat_uuid: str | None = None,
    prompt: str | None = None,
    benchmark: bool = False,
) -> None:
    if benchmark is True and prompt is None:
        click.secho("Error: Benchmark mode requires a prompt.", fg="red")
        return

    current_working_directory = os.getcwd()

    if not chat_uuid:
        try:
            async with RemoteExecutionClient.session(
                api_key, base_api_url, current_working_directory
            ) as client:
                chat = await client.create_chat()
                chat_uuid = chat.chat_uuid
        except httpx.ConnectError as e:
            click.secho(f"Error: {e}", fg="red")
            return

    click.echo()
    click.secho("△ Exponent v1.0.0", fg=(180, 150, 255), bold=True)
    click.echo()
    click.echo(
        " - Link: " + click.style(f"{base_url}/chats/{chat_uuid}", fg=(100, 200, 255))
    )
    click.echo(click.style("  - Shell: /bin/zsh", fg="white"))
    click.echo()
    click.echo(click.style("✓", fg="green", bold=True) + " Ready in 1401ms")

    # Open the chat in the browser
    if not benchmark and not prompt and not chat_uuid:
        click.launch(f"{base_url}/chats/{chat_uuid}")

    use_tools_config = UseToolsConfig()
    async with RemoteExecutionClient.session(
        api_key, base_api_url, current_working_directory
    ) as client:
        if benchmark:
            assert prompt is not None
            await asyncio.gather(
                start_chat(
                    client, chat_uuid, prompt, use_tools_config=use_tools_config
                ),
                run_execution_client(client, chat_uuid),
                benchmark_mode_exit(client, chat_uuid),
                heartbeat_thread(client, chat_uuid),
            )
        elif prompt:
            await asyncio.gather(
                start_chat(
                    client, chat_uuid, prompt, use_tools_config=use_tools_config
                ),
                run_execution_client(client, chat_uuid),
                heartbeat_thread(client, chat_uuid),
            )
        else:
            await asyncio.gather(
                run_execution_client(client, chat_uuid),
                heartbeat_thread(client, chat_uuid),
            )


async def run_execution_client(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        execution_requests = await client.get_execution_requests(chat_uuid)
        for execution_request in execution_requests:
            click.echo(f"Handling {execution_request.namespace} request:")
            click.echo(f"  - {execution_request}")
            execution_response = await client.handle_request(execution_request)
            click.echo(f"Posting {execution_request.namespace} response.")
            await client.post_execution_result(chat_uuid, execution_response)
        await asyncio.sleep(0.2)


async def start_chat(
    client: RemoteExecutionClient,
    chat_uuid: str,
    prompt: str,
    use_tools_config: UseToolsConfig,
) -> None:
    click.secho("Starting chat...")
    await client.start_chat(chat_uuid, prompt, use_tools_config=use_tools_config)
    click.secho("Chat started. Open the link to join the chat.")


async def benchmark_mode_exit(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        await asyncio.sleep(5)
        if await client.check_cli_execution_end_event(chat_uuid):
            sys.exit(0)


async def heartbeat_thread(client: RemoteExecutionClient, chat_uuid: str) -> None:
    while True:
        await client.send_heartbeat(chat_uuid)
        await asyncio.sleep(1)


def set_log_level() -> None:
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level), stream=sys.stdout)


if __name__ == "__main__":
    cli()
