import logging
import shutil
import typing
from copy import deepcopy
from pathlib import Path
from typing import Any
from unittest.mock import patch

import typer
import yaml
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal.migration.utils import _process_properties
from amsdal.schemas.manager import SchemaManager
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY
from amsdal_data.table_schemas.constants import SECONDARY_PARTITION_KEY
from amsdal_data.table_schemas.manager import TableSchemasManager
from amsdal_models.classes.model import Model
from amsdal_models.enums import BaseClasses
from amsdal_models.schemas.data_models.schema import ObjectSchema
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableSchema
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.singleton import Singleton
from rich import print
from typer import Option

from amsdal_cli.commands.cloud.app import cloud_sub_app
from amsdal_cli.commands.cloud.environments.utils import get_current_env
from amsdal_cli.commands.serve import utils
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_error
from amsdal_cli.utils.text import rich_highlight
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


@cloud_sub_app.command(name='sync-db, sync_db, sdb')
def sync_db_command(
    ctx: typer.Context,
    env_name: typing.Annotated[
        typing.Optional[str],  # noqa: UP007
        Option('--env', help='Environment name. Default is the current environment from configratuion.'),
    ] = None,
    *,
    skip_expose_db: bool = typer.Option(False, '-s', help='Skip exposing the database'),
) -> None:
    """
    Recreate local database from the remote one.
    """

    cli_config: CliConfig = ctx.meta['config']
    env_name = env_name or get_current_env(cli_config)

    if cli_config.verbose:
        print(rich_info(f'Syncing database for environment: {rich_highlight(env_name)}'))

    config_path: Path
    if not skip_expose_db:
        AmsdalConfigManager().load_config(Path('./config.yml'))
        manager = AmsdalManager()
        manager.authenticate()

        creds: dict[str, str] = _load_credentials(manager, cli_config, env_name)
        _expose_db(manager, cli_config, env_name)

        Singleton.invalidate(Singleton)  # type: ignore[arg-type]
        config_path = _build_config(creds)
    else:
        config_path = Path('sync-config.yml')

    _init_app(config_path)
    _copy_data()


def _init_app(config_path: Path) -> None:
    print(rich_info('Initializing app...'), end='')
    logging.disable(logging.WARNING)

    with patch.object(utils, 'print'):
        # delete the old warehouse
        if Path('warehouse').exists():
            shutil.rmtree(str(Path('warehouse').resolve()))
        output_path = Path('.')
        app_source_path = Path('src')

        amsdal_manager = utils.build_app_and_check_migrations(
            output_path=output_path,
            app_source_path=app_source_path,
            config_path=config_path,
            apply_fixtures=False,
            confirm_migrations=False,
        )
        amsdal_manager.build_static_files(app_source_path)
        amsdal_manager.post_setup()
        object_schema = SchemaManager().get_schema_by_name('Object', SchemaTypes.TYPE)
        _create_table('sqlite_state', object_schema, class_version='')  # type: ignore[arg-type]

        amsdal_manager.init_classes()

    print(rich_success('OK'))


def _load_credentials(manager: AmsdalManager, cli_config: CliConfig, env_name: str) -> dict[str, str]:
    print(rich_info('Receiving credentials... '), end='')

    try:
        list_response = manager.cloud_actions_manager.list_secrets(
            with_values=True,
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(rich_error(str(e)))
        raise typer.Exit(1) from e

    secrets = {}

    if list_response.secrets:
        for secret in list_response.secrets:
            secret_name, secret_value = secret.split('=', 1)
            secrets[secret_name] = secret_value

    print(rich_success('OK'))

    return secrets


def _expose_db(manager: AmsdalManager, cli_config: CliConfig, env_name: str) -> None:
    print(rich_info('Exposing database...'), end='')
    try:
        manager.cloud_actions_manager.expose_db(
            env_name=env_name,
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            ip_address=None,
        )
    except AmsdalCloudError as e:
        print(rich_error(str(e)))
        raise typer.Exit(1) from e

    print(rich_success('OK'))


def _build_config(secrets: dict[str, str]) -> Path:
    print(rich_info('Building config...'), end='')

    with open('config.yml') as _f:
        _origin_config = yaml.safe_load(_f)

    _config: Path = Path('sync-config.yml')
    _dns_historical = f'postgresql://{secrets["POSTGRES_USER"]}:{secrets["POSTGRES_PASSWORD"]}@{secrets["POSTGRES_HOST"]}:{secrets["POSTGRES_PORT"]}/{secrets["POSTGRES_DATABASE"]}'
    _dns_state = f'postgresql://{secrets["POSTGRES_STATE_USER"]}:{secrets["POSTGRES_STATE_PASSWORD"]}@{secrets["POSTGRES_STATE_HOST"]}:{secrets["POSTGRES_STATE_PORT"]}/{secrets["POSTGRES_STATE_DATABASE"]}'
    sqlite_history_db_path = './warehouse/amsdal_historical.sqlite3'
    sqlite_state_db_path = './warehouse/amsdal_state.sqlite3'

    for conn in _origin_config['connections']:
        if conn['name'] == _origin_config['resources_config']['lakehouse']:
            sqlite_history_db_path = conn['credentials'][0]['db_path']
        elif conn['backend'] == _origin_config['resources_config']['repository']['default']:
            sqlite_state_db_path = conn['credentials'][0]['db_path']

    _config_content = (
        CONFIG_TMPL.replace('{{app_name}}', _origin_config['application_name'])
        .replace('{{dns_historical}}', _dns_historical)
        .replace('{{dns_state}}', _dns_state)
        .replace('{{sqlite_history_db_path}}', sqlite_history_db_path)
        .replace('{{sqlite_state_db_path}}', sqlite_state_db_path)
        .strip()
    )
    _config.write_text(_config_content)
    print(rich_success('OK'))

    return _config


def _create_table(resource: str, object_schema: ObjectSchema, class_version: str | Versions) -> None:
    for prop_name, prop in object_schema.properties.items():  # type: ignore
        prop.field_name = prop_name
        prop.field_id = prop_name

    class_name = object_schema.title
    address = Address(
        resource=resource, class_name=class_name, class_version=class_version, object_id='', object_version=''
    )
    schema = TableSchema(
        address=address,
        columns=_process_properties(object_schema.properties, object_schema.required),
        indexed=[],
        unique_columns=[],
    )

    TableSchemasManager().register_table(schema)


def _copy_data() -> None:
    from models.type.object import Object  # type: ignore

    class_objects: list[Model] = []
    class_meta_objects: list[Model] = []
    _obj: Model

    for _obj in Object.objects.using('remote_historical').execute():
        _obj_copied = Object(
            _object_id=_obj.object_id,
            _object_version=_obj.object_version,
            **_obj.model_dump_refs(),
        )
        _obj_copied.save(force_insert=True, skip_hooks=True)

        if _obj.meta_class == 'TypeMeta':
            continue

        if _obj.object_id == BaseClasses.CLASS_OBJECT:
            class_objects.append(_obj)
        elif _obj.object_id == BaseClasses.CLASS_OBJECT_META:
            class_meta_objects.append(_obj)

    # copy metadata
    _copy_history_raw_data(
        from_address=Address(
            resource='remote_historical',
            class_name='metadata',
            class_version='',
            object_id='',
            object_version='',
        ),
        to_address=Address(
            resource='sqlite_history',
            class_name='metadata',
            class_version='',
            object_id='',
            object_version='',
        ),
    )

    # copy references
    _copy_history_raw_data(
        from_address=Address(
            resource='remote_historical',
            class_name='reference',
            class_version='',
            object_id='',
            object_version='',
        ),
        to_address=Address(
            resource='sqlite_history',
            class_name='reference',
            class_version='',
            object_id='',
            object_version='',
        ),
    )

    # copy migrations
    _copy_history_raw_data(
        from_address=Address(
            resource='remote_historical',
            class_name='migration',
            class_version='',
            object_id='',
            object_version='',
        ),
        to_address=Address(
            resource='sqlite_history',
            class_name='migration',
            class_version='',
            object_id='',
            object_version='',
        ),
    )
    _copy_state_raw_data(
        from_address=Address(
            resource='remote_state',
            class_name='migration',
            class_version='',
            object_id='',
            object_version='',
        ),
        to_address=Address(
            resource='sqlite_state',
            class_name='migration',
            class_version='',
            object_id='',
            object_version='',
        ),
    )

    class_id: Versions | str
    class_version: Versions | str
    for _obj in sorted(class_meta_objects, key=lambda obj: int(obj.get_metadata().is_latest)):
        _schema = ObjectSchema(**_obj.model_dump_refs())
        class_id = _obj.object_id  # type: ignore[assignment]
        class_version = _obj.object_version  # type: ignore[assignment]

        _create_table('sqlite_history', _schema, class_version=class_version)
        _copy_history_raw_data(
            from_address=Address(
                resource='remote_historical',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
            to_address=Address(
                resource='sqlite_history',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
        )

        if not _obj.get_metadata().is_latest:
            continue

        _create_table('sqlite_state', _schema, class_version=class_version)
        _copy_state_raw_data(
            from_address=Address(
                resource='remote_state',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
            to_address=Address(
                resource='sqlite_state',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
        )

    for _obj in sorted(class_objects, key=lambda obj: int(obj.get_metadata().is_latest)):
        _schema = ObjectSchema(**_obj.model_dump_refs())
        class_id = _obj.object_id  # type: ignore[assignment]
        class_version = _obj.object_version  # type: ignore[assignment]

        _create_table('sqlite_history', _schema, class_version=class_version)

        _copy_history_raw_data(
            from_address=Address(
                resource='remote_historical',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
            to_address=Address(
                resource='sqlite_history',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
            is_nested_table=True,
        )

        if not _obj.get_metadata().is_latest:
            continue

        _create_table('sqlite_state', _schema, class_version=class_version)
        _copy_state_raw_data(
            from_address=Address(
                resource='remote_state',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
            to_address=Address(
                resource='sqlite_state',
                class_name=class_id,
                class_version=class_version,
                object_id='',
                object_version='',
            ),
            is_nested_table=True,
        )


def _copy_history_raw_data(
    from_address: Address,
    to_address: Address,
    *,
    is_nested_table: bool = False,
) -> None:
    _conn_manager = AmsdalManager()._connections_manager
    _remote_conn = _conn_manager.get_connection(from_address.resource)
    items: list[dict[str, Any]] = _remote_conn.query(address=from_address)
    _conn = _conn_manager.get_connection(to_address.resource)

    for item in items:
        _conn.begin()
        _insert_data = deepcopy(item)
        _object_id = _insert_data.pop('_object_id')
        _object_version = _insert_data.pop('_object_version', None)
        _insert_data[PRIMARY_PARTITION_KEY] = _object_id

        if _object_version is not None:
            _insert_data[SECONDARY_PARTITION_KEY] = _object_version
        _conn.put(
            address=to_address.model_copy(
                update={
                    'object_id': item['_object_id'],
                    'object_version': item.get('_object_version', ''),
                }
            ),
            data=_insert_data,
        )
        _conn.commit()

        if is_nested_table:
            _create_table(
                'sqlite_history',
                ObjectSchema(**{'title': item['_object_id'], **item}),
                class_version=item.get('_object_version', ''),
            )

            _copy_history_raw_data(
                from_address=Address(
                    resource=from_address.resource,
                    class_name=item['_object_id'],
                    class_version=item.get('_object_version', ''),
                    object_id='',
                    object_version='',
                ),
                to_address=Address(
                    resource=to_address.resource,
                    class_name=item['_object_id'],
                    class_version=item.get('_object_version', ''),
                    object_id='',
                    object_version='',
                ),
            )


def _copy_state_raw_data(
    from_address: Address,
    to_address: Address,
    *,
    is_nested_table: bool = False,
) -> None:
    _conn_manager = AmsdalManager()._connections_manager
    _remote_conn = _conn_manager.get_connection(from_address.resource)
    items: list[dict[str, Any]] = _remote_conn.query(address=from_address)
    _conn = _conn_manager.get_connection(to_address.resource)

    for item in items:
        _conn.begin()
        _insert_data = deepcopy(item)
        _object_id = _insert_data.pop('_object_id')
        _insert_data.pop('_object_version', None)
        _insert_data[PRIMARY_PARTITION_KEY] = _object_id

        _conn.insert(
            address=to_address.model_copy(
                update={
                    'object_id': item['_object_id'],
                    'object_version': item.get('_object_version', ''),
                }
            ),
            data=_insert_data,
        )
        _conn.commit()

        if is_nested_table:
            _create_table(
                'sqlite_state',
                ObjectSchema(**{'title': item['_object_id'], **item}),
                class_version=item.get('_object_version', ''),
            )

            if item['_metadata']['next_version']:
                continue

            _copy_state_raw_data(
                from_address=Address(
                    resource=from_address.resource,
                    class_name=item['_object_id'],
                    class_version=item.get('_object_version', ''),
                    object_id='',
                    object_version='',
                ),
                to_address=Address(
                    resource=to_address.resource,
                    class_name=item['_object_id'],
                    class_version=item['_object_version'],
                    object_id='',
                    object_version='',
                ),
            )


CONFIG_TMPL = """
application_name: {{app_name}}
connections:
  - name: sqlite_history
    backend: sqlite-historical
    credentials:
      - db_path: {{sqlite_history_db_path}}
      - check_same_thread: false
  - name: sqlite_state
    backend: amsdal_data.connections.implementations.sqlite_state.SqliteStateConnection
    credentials:
      - db_path: {{sqlite_state_db_path}}
      - check_same_thread: false
  - name: remote_historical
    backend: postgres-historical
    credentials:
      dsn: {{dns_historical}}
  - name: remote_state
    backend: postgres-state
    credentials:
      dsn: {{dns_state}}
  - name: lock
    backend: amsdal_data.lock.implementations.thread_lock.ThreadLock
resources_config:
  lakehouse: sqlite_history
  lock: lock
  repository:
    default: sqlite_state
"""
