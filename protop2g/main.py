"""
protop2g
Copyright (C) 2022-2023 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source
code or documentation are not subject to the GNU General Public
License and may only be used or replicated with the express permission
of Red Hat, Inc.
"""


import click

from protop2g import __version__ as versobjc
from protop2g.view.repo import showrepo
from protop2g.view.stat import showstat
from protop2g.view.tkts import showtkts
from protop2g.work.keep import keepbrcs, keeptkts, storeinf


@click.group(name="protop2g")
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
        "protop2g by Akashdeep Dhar <t0xic0der@fedoraproject.org>",
        fg="green",
        bold=True,
    ),
)
def main(srce, dest, pkey, gkey, fusr, tusr):
    """
    Pagure Exporter
    """
    storeinf(srce, dest, pkey, gkey, fusr, tusr)


@main.command(
    name="tkts",
    help="Initiate transfer of issue tickets",
    context_settings={"show_default": True},
)
@click.option(
    "-s",
    "--status",
    type=click.Choice(["OPEN", "SHUT", "FULL"], case_sensitive=False),
    help="Extract issue tickets of the mentioned status",
    multiple=False,
    default="OPEN",
)
@click.option(
    "-r",
    "--ranges",
    nargs=2,
    help="Extract issue tickets in the mentioned ranges",
    default=None,
)
@click.option(
    "-p",
    "--select",
    type=str,
    help="Extract issue tickets of the selected numbers",
    default=None,
)
@click.option(
    "-c",
    "--comments",
    help="Transfer all the associated comments",
    default=False,
    is_flag=True,
)
@click.option(
    "-l",
    "--labels",
    help="Migrate all the associated labels",
    default=False,
    is_flag=True,
)
@click.option(
    "-a",
    "--commit",
    help="Assert issue ticket states as they were",
    default=False,
    is_flag=True,
)
def main_transfer_tkts(status, select, ranges, comments, labels, commit):
    if select is not None and ranges is not None:
        raise click.UsageError("The `select` and `ranges` options cannot be used together")

    tktgroup = []

    if select is not None:
        try:
            tktgroup = [int(indx.strip()) for indx in select.split(",")]
        except Exception as expt:
            raise click.BadParameter(
                message="The provided parameters for the `select` option could not be parsed"
            ) from expt

    if ranges is not None:
        try:
            tktgroup = [indx for indx in range(min(int(ranges)), max(int(ranges)) + 1)]
        except Exception as expt:
            raise click.BadParameter(
                message="The provided parameters for the `ranges` option could not be parsed"
            ) from expt

    keeptkts(status, tktgroup, comments, labels, commit)
    showstat()
    showtkts()


@main.command(
    name="repo",
    help="Initialize transfer of repository assets",
    context_settings={"show_default": True},
)
@click.option("-b", "--brcs", "brcs", multiple=True, help="List of branches to extract")
def main_transfer_repo(brcs):
    keepbrcs(brcs)
    showstat()
    showrepo()
