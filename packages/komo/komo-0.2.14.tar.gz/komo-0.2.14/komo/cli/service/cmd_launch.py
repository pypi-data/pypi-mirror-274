import os
from typing import Optional

import click
import yaml

from komo import printing
from komo.core import launch_service
from komo.types import Cloud, ServiceConfig


@click.command("launch")
@click.option("--gpus", type=str, default=None)
@click.option("--cloud", "-c", type=str, default=None)
@click.option("--name", type=str, required=True)
@click.argument("config_file", nargs=1)
def cmd_launch(
    gpus: Optional[str],
    cloud: Optional[str],
    name: str,
    config_file: str,
):
    if not os.path.isfile(config_file):
        printing.error(f"{config_file} does not exist")
        exit(1)

    service_config = ServiceConfig.from_yaml(config_file)
    if gpus:
        service_config.resources["gpus"] = gpus
    if cloud:
        service_config.cloud = Cloud(cloud)

    service = launch_service(
        service_config,
        name,
    )

    printing.success(f"Succesfully launched service {service.name}")
