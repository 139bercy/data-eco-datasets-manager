import click

from common import make_bytes_size_human_readable


@click.group("tools")
def tools():
    """Some useful tools"""


@tools.command("convert-size")
@click.argument("bytes")
def convert_size(bytes):
    result = make_bytes_size_human_readable(int(bytes))
    print(f"{bytes} octets => {result}")