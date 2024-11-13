import click
from adapters.cli.endpoints.dataset import dataset
from adapters.cli.endpoints.db import database
from adapters.cli.endpoints.publishers import get_publishers
from adapters.cli.endpoints.users import users
from adapters.cli.endpoints.groups import groups
from adapters.cli.endpoints.tools import tools


@click.group()
def cli():
    """Application adapters.cli"""


cli.add_command(dataset)
cli.add_command(database)
cli.add_command(get_publishers)
cli.add_command(groups)
cli.add_command(users)
cli.add_command(tools)
