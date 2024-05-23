from pathlib import Path

import typer
from rich import print

from amsdal_cli.utils.text import CustomConfirm
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


def build_config_file(
    output_path: Path,
    config_path: Path,
    *,
    no_input: bool,
) -> None:
    print(rich_info('Building config.yml file...'), end=' ')

    if not config_path.exists() or not config_path.name.endswith('.yml'):
        print(rich_error(f'\nConfig file "{config_path.resolve()}" does not exist or has wrong extension.'))
        raise typer.Exit(1)

    config_destination = output_path / 'config.yml'

    if (
        no_input
        or not config_destination.exists()
        or (
            CustomConfirm.ask(
                rich_info(
                    f'\nThe config file "{config_destination.resolve()}" already exists. '
                    'Would you like to overwrite it?'
                ),
                default=False,
                show_default=False,
                choices=['y', 'N'],
            )
        )
    ):
        config_destination.parent.mkdir(parents=True, exist_ok=True)
        config_destination.touch(exist_ok=True)

        with config_path.open('rt') as _file:
            config_destination.write_text(_file.read())

    print(rich_success('OK!'))
