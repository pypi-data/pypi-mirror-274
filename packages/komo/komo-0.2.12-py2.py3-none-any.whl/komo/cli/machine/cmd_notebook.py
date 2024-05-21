import webbrowser

import click

from komo import printing
from komo.core import get_machine
from komo.types import MachineStatus


@click.command("notebook")
@click.argument(
    "machine_name",
    type=str,
)
def cmd_notebook(machine_name: str):
    machine = get_machine(machine_name)
    url = machine.notebook_url
    printing.success(f"Opening notebook at {url}")
    webbrowser.open(url)
