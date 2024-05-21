import os
from typing import List, Optional

import click
import textwrap3
from tabulate import tabulate

from komo import printing
from komo.core import list_services


@click.command("list")
def cmd_list():
    services = list_services()
    services_to_print = [
        [
            service.name,
            service.status.value,
            textwrap3.fill(
                service.status_message,
                width=50,
                replace_whitespace=False,
                drop_whitespace=False,
            ),
        ]
        for service in services
    ]

    printing.header(f"Found {len(services)} Komodo services\n", bold=True)
    printing.info(
        tabulate(
            services_to_print,
            headers=[
                "Name",
                "Status",
                "Message",
            ],
            tablefmt="simple_grid",
        ),
    )
