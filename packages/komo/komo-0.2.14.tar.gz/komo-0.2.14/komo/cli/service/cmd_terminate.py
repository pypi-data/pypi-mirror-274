import click

from komo import printing
from komo.core import terminate_service


@click.command("terminate")
@click.argument(
    "service_name",
    type=str,
)
def cmd_terminate(service_name: str):
    terminate_service(service_name)
    printing.success(f"Service {service_name} is being terminated")
