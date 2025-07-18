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


import pytest
from click.testing import CliRunner

from pagure_exporter.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--help",
            0,
            [
                "Usage: pagure_exporter [OPTIONS] COMMAND [ARGS]...",
                "Options:",
                "Pagure Exporter",
                "Source namespace for importing assets from",
                "Destination namespace for exporting assets to",
                "Pagure API key for accessing the source namespace",
                "GitLab API key for accessing the destination namespace",
                "Username of the account that owns the Pagure API key",
                "Username of the account that owns the GitLab API key",
                "Show the version and exit.",
                "Show this message and exit.",
            ],
            id="Basic help",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a tkts --help",
            0,
            [
                "Usage: pagure_exporter tkts [OPTIONS]",
                "Initiate transfer of issue tickets",
                "Options:",
                "Extract issue tickets of the mentioned status",
                "Extract issue tickets in the mentioned ranges",
                "Extract issue tickets of the selected numbers",
                "Transfer all the associated comments",
                "Migrate all the associated labels",
                "Assert issue ticket states as they were",
                "Show this message and exit.",
            ],
            id="Tickets help",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a repo --help",
            0,
            [
                "Usage: pagure_exporter repo [OPTIONS]",
                "Initialize transfer of repository assets",
                "Options:",
                "List of branches to extract",
                "List of tags to extract",
                "Show this message and exit.",
            ],
            id="Repositories help",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a tkts --select 4,2,0 --ranges 6 9",
            2,
            [
                "Usage: pagure_exporter tkts [OPTIONS]",
                "Try 'pagure_exporter tkts --help' for help.",
                "Error: The `select` and `ranges` options cannot be used together",
            ],
            id="Using `select` and `ranges` options together",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a tkts --select string",
            2,
            [
                "Usage: pagure_exporter tkts [OPTIONS]",
                "Try 'pagure_exporter tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `select` option could not be parsed",  # noqa: E501
            ],
            id="Providing invalid string input to the `select` option",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a tkts --ranges strA strB",
            2,
            [
                "Usage: pagure_exporter tkts [OPTIONS]",
                "Try 'pagure_exporter tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `ranges` option could not be parsed",  # noqa: E501
            ],
            id="Providing invalid string input to the `ranges` option",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a tkts --select",
            2,
            ["Error: Option '--select' requires an argument."],
            id="Providing empty input to the `select` option",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a tkts --ranges",
            2,
            ["Error: Option '--ranges' requires 2 arguments."],
            id="Providing empty input to the `ranges` option",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a repo --brcs",
            2,
            ["Error: Option '--brcs' requires an argument."],
            id="Providing empty input to the `brcs` option",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a repo --tags",
            2,
            ["Error: Option '--tags' requires an argument."],
            id="Providing empty input to the `tags` option",
        ),
        pytest.param(
            "-a a -b a -s a -d a -p a -g a -f a -t a",
            2,
            [
                "Usage: pagure_exporter [OPTIONS] COMMAND [ARGS]...",
                "Try 'pagure_exporter --help' for help.",
                "Error: Missing command.",
            ],
            id="Providing empty input for the commands",
        ),
    ],
)
def test_main_help(cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in result.output  # noqa: S101
