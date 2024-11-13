import click

from common import format_filename
from core.configuration import DATABASE
from core.output import to_csv
from datasets.usecases import search_resources
from services import security
from users.repositories import TinyDbUserRepository
from users.usecases import create_user


@click.group("users")
def users():
    """Manage users"""


@users.command("create")
@click.option("--email", "-e", required=True, help="User email")
@click.option("--groups", "-g", required=True, multiple=True, help="User group")
def api_create_user(email, groups):
    """Create user"""
    create_user(email, groups)
    raise NotImplementedError


@users.command("export")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def export_users_to_csv(quotes):
    """List and export users"""
    # /!\ Les ressources sont exportées directement en CSV par ODS
    data = security.get_users()
    headers = data[0].keys()
    filename = format_filename(f"users.csv", "data")
    to_csv(report=data, filename=filename, headers=headers, quotes=quotes)


@users.command("search")
@click.argument("chain")
@click.option("--field", "-f", default="username", help="Field for research")
@click.option("--detail", "-d", is_flag=True, default=False, help="Print resources details")
@click.option("--export", "-e", is_flag=True, default=False, help="Export resources to csv")
@click.option("--header", "-h", help="Custom headers for exports", multiple=True)
@click.option("--sort", "-s", help="Sort by (-)field")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def search_users(chain, field, detail, export, header, sort, quotes):
    """Search users"""
    repository = TinyDbUserRepository(DATABASE)
    results = search_resources(chain=chain, detail=detail, field=field, repository=repository, sort=sort)
    headers = list(header) if len(header) != 0 else results[0].keys()
    if export:
        output = format_filename(f"users-{field}-{chain}.csv", "data")
        to_csv(report=results, filename=output, headers=headers, quotes=quotes)