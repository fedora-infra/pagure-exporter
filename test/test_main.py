import pytest
from click.testing import CliRunner

from protop2g.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--help",
            0,
            [
                "Usage: protop2g [OPTIONS] COMMAND [ARGS]...",
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
            "-s a -d a -p a -g a -f a -t a tkts --help",
            0,
            [
                "Usage: protop2g tkts [OPTIONS]",
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
            "-s a -d a -p a -g a -f a -t a repo --help",
            0,
            [
                "Usage: protop2g repo [OPTIONS]",
                "Initialize transfer of repository assets",
                "Options:",
                "List of branches to extract",
                "Show this message and exit.",
            ],
            id="Repositories help",
        ),
        pytest.param(
            "-s a -d a -p a -g a -f a -t a tkts --select 4,2,0 --ranges 6 9",
            2,
            [
                "Usage: protop2g tkts [OPTIONS]",
                "Try 'protop2g tkts --help' for help.",
                "Error: The `select` and `ranges` options cannot be used together",
            ],
            id="Using `select` and `ranges` options together",
        ),
        pytest.param(
            "-s a -d a -p a -g a -f a -t a tkts --select string",
            2,
            [
                "Usage: protop2g tkts [OPTIONS]",
                "Try 'protop2g tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `select` option could not be parsed",  # noqa: E501
            ],
            id="Providing invalid string input to the `select` option",
        ),
        pytest.param(
            "-s a -d a -p a -g a -f a -t a tkts --ranges strA strB",
            2,
            [
                "Usage: protop2g tkts [OPTIONS]",
                "Try 'protop2g tkts --help' for help.",
                "Error: Invalid value: The provided parameters for the `ranges` option could not be parsed",  # noqa: E501
            ],
            id="Providing invalid string input to the `ranges` option",
        ),
        pytest.param(
            "-s a -d a -p a -g a -f a -t a tkts --select",
            2,
            ["Error: Option '--select' requires an argument."],
            id="Providing empty input to the `select` option",
        ),
        pytest.param(
            "-s a -d a -p a -g a -f a -t a tkts --ranges",
            2,
            ["Error: Option '--ranges' requires 2 arguments."],
            id="Providing empty input to the `ranges` option",
        ),
        pytest.param(
            "-s a -d a -p a -g a -f a -t a repo --brcs",
            2,
            ["Error: Option '--brcs' requires an argument."],
            id="Providing empty input to the `brcs` option",
        ),
        pytest.param(
            "-s a -d a -p a -g a -f a -t a",
            2,
            [
                "Usage: protop2g [OPTIONS] COMMAND [ARGS]...",
                "Try 'protop2g --help' for help.",
                "Error: Missing command.",
            ],
        ),
    ],
)
def test_main_help(cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in result.output  # noqa: S101
