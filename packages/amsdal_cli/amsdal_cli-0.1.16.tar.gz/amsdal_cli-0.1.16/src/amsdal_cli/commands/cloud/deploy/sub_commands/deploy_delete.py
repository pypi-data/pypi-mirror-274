from pathlib import Path

from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.deploy.app import deploy_sub_app
from amsdal_cli.commands.cloud.deploy.app import deprecated_deploy_sub_app
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_success


@deploy_sub_app.command(name='delete, del, d')
@deprecated_deploy_sub_app.command(name='destroy', deprecated=True)
def destroy_command(deployment_id: str) -> None:
    """
    Destroy the app on the Cloud Server.
    """
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.destroy_deploy(deployment_id)
    except AmsdalCloudError as e:
        print(rich_error(str(e)))
        return

    print(
        rich_success(
            'Destroying process is in progress now. '
            'After a few minutes, you can check the status of your deployment.'
        )
    )
