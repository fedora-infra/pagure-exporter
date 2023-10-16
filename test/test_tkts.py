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


from os import environ as envr

import pytest
from click.testing import CliRunner

from protop2g.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with OPEN status without labels, without states and without comments",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with SHUT status without labels, without states and without comments",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with FULL status without labels, without states and without comments",  # noqa: E501
        ),
        pytest.param(
            f"--srce ZEROEXISTENT --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts",  # noqa: E501
            1,
            [
                "[ FAIL ] Source namespace metadata acquisition failed!",
                "The namespace metadata could not be acquired.",
                "Code: 404",
                "Reason: NOT FOUND",
            ],
            id="Transferring issue tickets from a source namespace that does not exist",
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest ZEROEXISTENT --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN",  # noqa: E501
            1,
            [
                "[ FAIL ] Destination namespace metadata acquisition failed!",
                "The namespace metadata could not be acquired.",
                "Code: 404",
                "Reason: Not Found",
            ],
            id="Transferring issue tickets to a destination namespace that does not exist",
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --commit",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, with states and without comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Asserting issue ticket status...",
                "Assertion unnecessary due to the OPEN status of the ticket",
            ],
            id="Transferring issue tickets with OPEN status along with states but without comments and without labels",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --commit",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, with states and without comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
            ],
            id="Transferring issue tickets with SHUT status along with states but without comments and without labels",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --commit",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, with states and without comments off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Asserting issue ticket status...",
                "Assertion unnecessary due to the OPEN status of the ticket",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
            ],
            id="Transferring issue tickets with FULL status along with states but without comments and without labels",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --labels",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets with labels, without states and without comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket with labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with OPEN status along with labels but without states and without comments",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --labels",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets with labels, without states and without comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket with labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with SHUT status along with labels but without states and without comments",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --labels",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets with labels, without states and without comments off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket with labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Migrating issue ticket with labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with FULL status along with labels but without states and without comments",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --comments",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states and with comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Reading comment information...",
                "Found 3 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 3)...",
                "Transferred to ",
            ],
            id="Transferring issue tickets with OPEN status along with comments but without labels and without states",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --comments",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states and with comments off the given selection",  # noqa: E501
                "Found 1 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Reading comment information...",
                "Found 4 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 4)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 4)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 4)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 4 of 4)...",
                "Transferred to ",
            ],
            id="Transferring issue tickets with SHUT status along with comments but without labels and without states",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --comments",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states and with comments off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Reading comment information...",
                "Found 3 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 3)...",
                "Transferred to ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Reading comment information...",
                "Found 4 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 4)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 4)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 4)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 4 of 4)...",
                "Transferred to ",
            ],
            id="Transferring issue tickets with FULL status along with comments but without labels and without states",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --ranges 1 2",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
            ],
            id="Transferring issue tickets with OPEN status without labels, without states and without comments the identities of which fall in the given range",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --ranges 1 2",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with SHUT status without labels, without states and without comments the identities of which fall in the given range",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --ranges 1 2",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with FULL status without labels, without states and without comments the identities of which fall in the given range",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --select 1,2",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
            ],
            id="Transferring issue tickets with OPEN status without labels, without states and without comments the identities of which fall in the given selection",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --select 1,2",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with SHUT status without labels, without states and without comments the identities of which fall in the given selection",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --select 1,2",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states and without comments off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with FULL status without labels, without states and without comments the identities of which fall in the given selection",  # noqa: E501
        ),
    ],
)
def test_main_tkts(caplog, cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101
