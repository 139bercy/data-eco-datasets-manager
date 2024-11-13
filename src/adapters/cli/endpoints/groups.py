import click

from common import format_filename
from core.configuration import AVAILABLE_PERMISSIONS, DEFAULT_GROUP_PERMISSIONS
from core.output import to_csv, sort_by_field
from services import security
from services.resources import create_group
from users.usecases import add_user_to_group


@click.group("groups")
def groups():
    """Manage groups"""


@groups.group("permissions")
def groups_permissions():
    """Manage groups permissions"""


@groups_permissions.command("list")
def list_groups_permissions():
    """List available groups permissions"""
    click.echo(click.style("Permissions:", fg="green"))
    for permission in enumerate(AVAILABLE_PERMISSIONS):
        click.echo(click.style(f"\t{permission[0] + 1} {permission[1]}", fg="green"))


@groups_permissions.command("update")
@click.argument("group_id")
@click.argument("title")
def api_update_group_permissions(group_id, title):
    """Update group with default permissions"""
    click.echo(click.style("Permissions:", fg="green"))
    for permission in DEFAULT_GROUP_PERMISSIONS:
        click.echo(click.style(f"\t{permission}", fg="green"))
    click.confirm('Do you want to continue?', abort=True)
    security.update_one_group_permissions(group_id=group_id, title=title, permissions=DEFAULT_GROUP_PERMISSIONS)


@groups.command("list")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
@click.option("--sort", "-s", help="Sort by (-)field")
def export_groups_to_csv(quotes, sort):
    """List and export groups"""
    data = security.get_groups()
    result = sort_by_field(data=data, field=sort)
    headers = [
        "created_at",
        "updated_at",
        "uid",
        "title",
        "description",
        "permissions",
        "management_limits",
        "explore_limits",
        "user_count",
    ]
    filename = format_filename(f"groups.csv", "data")
    to_csv(report=result, filename=filename, headers=headers, quotes=quotes)


@groups.command("create")
@click.argument("title")
@click.option("-p", "--permissions", help="Add specific permissions", multiple=True,
              type=click.Choice(AVAILABLE_PERMISSIONS))
def api_create_group(title, permissions):
    """Create group"""
    click.echo(click.style("A group will be created with these permissions:", fg="red"))
    for permission in enumerate(AVAILABLE_PERMISSIONS):
        click.echo(click.style(f"\t{permission[0] + 1} {permission[1]}", fg="green"))
    click.confirm(click.style('Do you want to continue?', fg="red"), abort=True)
    group_permissions = DEFAULT_GROUP_PERMISSIONS if not permissions else list(permissions)
    create_group(title=title, permissions=group_permissions)


@groups.command("add-user")
@click.argument("group_id")
@click.argument("username")
def api_group_add_user(group_id, username):
    """Add user to group"""
    add_user_to_group(group_id=group_id, username=username)
