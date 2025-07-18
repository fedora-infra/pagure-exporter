"""
Pagure Exporter
Copyright (C) 2022-2025 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source code or
documentation are not subject to the GNU General Public License and may only
be used or replicated with the express permission of Red Hat, Inc.
"""


import click

from . import __version__ as versobjc
from .conf import standard
from .view.repo import show_repo
from .view.stat import show_status
from .view.tkts import show_tickets
from .work.keep import keep_branches, keep_tags, keep_tickets, store_info


@click.group(
    name="pagure_exporter",
    context_settings={"show_default": True},
)
@click.option(
    "-a",
    "--splt",
    "splt",
    default=standard.forge_srce,
    help="Source hostname for accessing Pagure information",
)
@click.option(
    "-b",
    "--dplt",
    "dplt",
    default=standard.forge_dest,
    help="Destination hostname for accessing GitLab information",
)
@click.option(
    "-s",
    "--srce",
    "srce",
    required=True,
    help="Source namespace for importing assets from",
)
@click.option(
    "-d",
    "--dest",
    "dest",
    required=True,
    help="Destination namespace for exporting assets to",
)
@click.option(
    "-p",
    "--pkey",
    "pkey",
    required=True,
    help="Pagure API key for accessing the source namespace",
)
@click.option(
    "-g",
    "--gkey",
    "gkey",
    required=True,
    help="GitLab API key for accessing the destination namespace",
)
@click.option(
    "-f",
    "--fusr",
    "fusr",
    required=True,
    help="Username of the account that owns the Pagure API key",
)
@click.option(
    "-t",
    "--tusr",
    "tusr",
    required=True,
    help="Username of the account that owns the GitLab API key",
)
@click.version_option(
    version=versobjc,
    prog_name=click.style(
        "Pagure Exporter by Akashdeep Dhar <t0xic0der@fedoraproject.org>",
        fg="green",
        bold=True,
    ),
)
def main(splt, dplt, srce, dest, pkey, gkey, fusr, tusr):
    """
    Pagure Exporter
    """
    store_info(splt, dplt, srce, dest, pkey, gkey, fusr, tusr)


@main.command(
    name="tkts",
    help="Initiate transfer of issue tickets",
    context_settings={"show_default": True},
)
@click.option(
    "-s",
    "--status",
    "status",
    type=click.Choice(["OPEN", "SHUT", "FULL"], case_sensitive=False),
    help="Extract issue tickets of the mentioned status",
    default="OPEN",
)
@click.option(
    "-r",
    "--ranges",
    "ranges",
    nargs=2,
    help="Extract issue tickets in the mentioned ranges",
    default=None,
)
@click.option(
    "-p",
    "--select",
    "select",
    type=str,
    help="Extract issue tickets of the selected numbers",
    default=None,
)
@click.option(
    "-c",
    "--comments",
    "comments",
    help="Transfer all the associated comments",
    default=False,
    is_flag=True,
)
@click.option(
    "-l",
    "--labels",
    "labels",
    help="Migrate all the associated labels",
    default=False,
    is_flag=True,
)
@click.option(
    "-a",
    "--commit",
    "commit",
    help="Assert issue ticket states as they were",
    default=False,
    is_flag=True,
)
@click.option(
    "-t",
    "--secret",
    "secret",
    help="Confirm issue ticket privacy as they were",
    default=False,
    is_flag=True,
)
@click.option(
    "-o",
    "--series",
    "series",
    help="Ensure issue ticket sequence as they were",
    default=False,
    is_flag=True,
)
def main_transfer_tkts(status, select, ranges, comments, labels, commit, secret, series):
    if select is not None and ranges is not None:
        raise click.UsageError("The `select` and `ranges` options cannot be used together")

    ticket_group = []

    if select is not None:
        try:
            ticket_group = [int(indx.strip()) for indx in select.split(",")]
        except Exception as expt:
            raise click.BadParameter(
                message="The provided parameters for the `select` option could not be parsed"
            ) from expt

    if ranges is not None:
        try:
            ranges = [int(indx) for indx in ranges]
            ticket_group = [indx for indx in range(min(ranges), max(ranges) + 1)]
        except Exception as expt:
            raise click.BadParameter(
                message="The provided parameters for the `ranges` option could not be parsed"
            ) from expt

    keep_tickets(status, ticket_group, comments, labels, commit, secret, series)
    show_status()
    show_tickets()


@main.command(
    name="repo",
    help="Initialize transfer of repository assets",
    context_settings={"show_default": True},
)
@click.option("-b", "--brcs", "brcs", type=str, default=None, help="List of branches to extract")
@click.option("-t", "--tags", "tags", type=str, default=None, help="List of tags to extract")
def main_transfer_repo(brcs, tags):
    tag_list = branch_list = []

    if brcs is not None:
        branch_list = [indx.strip() for indx in brcs.split(",")]

    if tags is not None:
        tag_list = [indx.strip() for indx in tags.split(",")]

    keep_branches(branch_list)
    keep_tags(tag_list)
    show_status()
    show_repo()
