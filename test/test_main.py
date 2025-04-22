"""
Pagure Exporter
Copyright (C) 2022-2023 Akashdeep Dhar

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
                "Usage: pagure-exporter [OPTIONS] COMMAND [ARGS]...",
                "Pagure Exporter",
                "Options:",
                "--version",
                "Show the version and exit.",
                "--help",
                "Show this message and exit.",
                "Commands:",
                "forgejo",
                "Forgejo support for Pagure Exporter",
                "gitlab",
                "GitLab support for Pagure Exporter",
            ],
            id="General: Basic help",
        ),
        pytest.param(
            "--version",
            0,
            [
                "Pagure Exporter by Akashdeep Dhar <t0xic0der@fedoraproject.org>, version ",
            ],
            id="General: Basic version",
        ),
        pytest.param(
            "gitlab --help",
            0,
            [
                "Usage: pagure-exporter gitlab [OPTIONS] COMMAND [ARGS]...",
                "GitLab support for Pagure Exporter",
                "Options:",
                "-s, --srce TEXT",
                "Source namespace for importing assets from",
                "-d, --dest TEXT",
                "Destination namespace for exporting assets to",
                "-p, --skey TEXT",
                "Pagure API key for accessing the source namespace",
                "-g, --dkey TEXT",
                "GitLab API key for accessing the destination namespace",
                "-f, --susr TEXT",
                "Username of the account that owns the Pagure API key",
                "-t, --dusr TEXT",
                "Username of the account that owns the GitLab API key",
                "--help",
                "Show this message and exit.",
                "Commands:",
                "repo  Initialize transfer of repository assets",
                "tkts  Initiate transfer of issue tickets",
            ],
            id="GitLab: Help topics",
        ),
        pytest.param(
            "forgejo --help",
            0,
            [
                "Usage: pagure-exporter forgejo [OPTIONS] COMMAND [ARGS]...",
                "Forgejo support for Pagure Exporter",
                "Options:",
                "-s, --srce TEXT",
                "Source namespace for importing assets from",
                "-d, --dest TEXT",
                "Destination namespace for exporting assets to",
                "-p, --skey TEXT",
                "Pagure API key for accessing the source namespace",
                "-g, --dkey TEXT",
                "Forgejo API key for accessing the destination namespace",
                "-f, --susr TEXT",
                "Username of the account that owns the Pagure API key",
                "-t, --dusr TEXT",
                "Username of the account that owns the Forgejo API key",
                "--help",
                "Show this message and exit.",
                "Commands:",
                "repo  Initialize transfer of repository assets",
                "tkts  Initiate transfer of issue tickets",
            ],
            id="Forgejo: Help topics",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a tkts --help",
            0,
            [
                "Usage: pagure-exporter gitlab tkts [OPTIONS]",
                "Initiate transfer of issue tickets",
                "Options:",
                "-s, --status [OPEN|SHUT|FULL]",
                "Extract issue tickets of the mentioned status",
                "[default: OPEN]",
                "-r, --ranges TEXT...",
                "Extract issue tickets in the mentioned ranges",
                "-p, --select TEXT",
                "Extract issue tickets of the selected numbers",
                "-c, --comments",
                "Transfer all the associated comments",
                "-l, --labels",
                "Migrate all the associated labels",
                "-a, --commit",
                "Assert issue ticket states as they were",
                "-t, --secret",
                "Confirm issue ticket privacy as they were",
                "-o, --series",
                "Ensure issue ticket sequence as they were",
                "--help",
                "Show this message and exit.",
            ],
            id="GitLab: Tickets help",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a tkts --help",
            0,
            [
                "Usage: pagure-exporter forgejo tkts [OPTIONS]",
                "Initiate transfer of issue tickets",
                "Options:",
                "-s, --status [OPEN|SHUT|FULL]",
                "Extract issue tickets of the mentioned status",
                "[default: OPEN]",
                "-r, --ranges TEXT...",
                "Extract issue tickets in the mentioned ranges",
                "-p, --select TEXT",
                "Extract issue tickets of the selected numbers",
                "-c, --comments",
                "Transfer all the associated comments",
                "-l, --labels",
                "Migrate all the associated labels",
                "-a, --commit",
                "Assert issue ticket states as they were",
                "-t, --secret",
                "Confirm issue ticket privacy as they were",
                "-o, --series",
                "Ensure issue ticket sequence as they were",
                "--help",
                "Show this message and exit.",
            ],
            id="Forgejo: Tickets help",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a repo --help",
            0,
            [
                "Usage: pagure-exporter gitlab repo [OPTIONS]",
                "Initialize transfer of repository assets",
                "Options:",
                "-b, --brcs TEXT",
                "List of branches to extract",
                "--help",
                "Show this message and exit.",
            ],
            id="GitLab: Repositories help",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a repo --help",
            0,
            [
                "Usage: pagure-exporter forgejo repo [OPTIONS]",
                "Initialize transfer of repository assets",
                "Options:",
                "-b, --brcs TEXT",
                "List of branches to extract",
                "--help",
                "Show this message and exit.",
            ],
            id="Forgejo: Repositories help",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a tkts --select 4,2,0 --ranges 6 9",
            2,
            [
                "Usage: pagure-exporter gitlab tkts [OPTIONS]",
                "Try 'pagure-exporter gitlab tkts --help' for help.",
                "Error: The `select` and `ranges` options cannot be used together",
            ],
            id="GitLab: Using `select` and `ranges` options together"
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a tkts --select 4,2,0 --ranges 6 9",
            2,
            [
                "Usage: pagure-exporter forgejo tkts [OPTIONS]",
                "Try 'pagure-exporter forgejo tkts --help' for help.",
                "Error: The `select` and `ranges` options cannot be used together",
            ],
            id="Forgejo: Using `select` and `ranges` options together",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a tkts --select string",
            2,
            [
                "Usage: pagure-exporter gitlab tkts [OPTIONS]",
                "Try 'pagure-exporter gitlab tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `select` option could not be parsed",  # noqa: E501
            ],
            id="GitLab: Providing invalid string input to the `select` option",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a tkts --select string",
            2,
            [
                "Usage: pagure-exporter forgejo tkts [OPTIONS]",
                "Try 'pagure-exporter forgejo tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `select` option could not be parsed",  # noqa: E501
            ],
            id="Forgejo: Providing invalid string input to the `select` option",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a tkts --ranges strA strB",
            2,
            [
                "Usage: pagure-exporter gitlab tkts [OPTIONS]",
                "Try 'pagure-exporter gitlab tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `ranges` option could not be parsed",  # noqa: E501
            ],
            id="GitLab: Providing invalid string input to the `ranges` option",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a tkts --ranges strA strB",
            2,
            [
                "Usage: pagure-exporter forgejo tkts [OPTIONS]",
                "Try 'pagure-exporter forgejo tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `ranges` option could not be parsed",  # noqa: E501
            ],
            id="Forgejo: Providing invalid string input to the `ranges` option",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a tkts --select",
            2,
            ["Error: Option '--select' requires an argument."],
            id="GitLab: Providing empty input to the `select` option",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a tkts --select",
            2,
            ["Error: Option '--select' requires an argument."],
            id="Forgejo: Providing empty input to the `select` option",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a tkts --ranges",
            2,
            ["Error: Option '--ranges' requires 2 arguments."],
            id="GitLab: Providing empty input to the `ranges` option",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a tkts --ranges",
            2,
            ["Error: Option '--ranges' requires 2 arguments."],
            id="Forgejo: Providing empty input to the `ranges` option",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a repo --brcs",
            2,
            ["Error: Option '--brcs' requires an argument."],
            id="GitLab: Providing empty input to the `brcs` option",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a repo --brcs",
            2,
            ["Error: Option '--brcs' requires an argument."],
            id="Forgejo: Providing empty input to the `brcs` option",
        ),
        pytest.param(
            "gitlab -s a -d a -p a -g a -f a -t a",
            2,
            [
                "Usage: pagure-exporter gitlab [OPTIONS] COMMAND [ARGS]...",
                "Try 'pagure-exporter gitlab --help' for help.",
                "Error: Missing command.",
            ],
            id="GitLab: Providing empty input for the commands",
        ),
        pytest.param(
            "forgejo -s a -d a -p a -g a -f a -t a",
            2,
            [
                "Usage: pagure-exporter forgejo [OPTIONS] COMMAND [ARGS]...",
                "Try 'pagure-exporter forgejo --help' for help.",
                "Error: Missing command.",
            ],
            id="Forgejo: Providing empty input for the commands",
        ),
    ],
)
def test_main_help(cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in result.output  # noqa: S101
