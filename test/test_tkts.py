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


from os import environ as envr

import pytest
from click.testing import CliRunner

from pagure_exporter.conf import standard
from pagure_exporter.main import main


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket without labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
            ],
            id="Transferring issue tickets with OPEN status without labels, without states, without privacy, without comments and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket without labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
            ],
            id="Transferring issue tickets with SHUT status without labels, without states, without privacy, without comments and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 4 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket without labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket without labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
            ],
            id="Transferring issue tickets with FULL status without labels, without states, without privacy, without comments and with order",  # noqa: E501
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
                "Code: 0",
                "Reason: 404: 404 Project Not Found",
            ],
            id="Transferring issue tickets to a destination namespace that does not exist",
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --commit --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, with states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Assertion unnecessary due to the OPEN status of the ticket",
                "[ BUSY ] Migrating issue ticket without labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Assertion unnecessary due to the OPEN status of the ticket",
            ],
            id="Transferring issue tickets with OPEN status along with states but without comments, without privacy, without labels and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --commit --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, with states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
                "[ BUSY ] Migrating issue ticket without labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
            ],
            id="Transferring issue tickets with SHUT status along with states but without comments, without privacy, without labels and with order",  # noqa: E501
        ),

        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --secret --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states, with privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket without labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
            ],
            id="Transferring issue tickets with OPEN status along with privacy but without states, without comments, without labels and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --secret --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states, with privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket without labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
            ],
            id="Transferring issue tickets with SHUT status along with privacy but without states, without comments, without labels and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --select 1 --commit --comments --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, with states, without privacy, with comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Asserting issue ticket status...",
                "Assertion unnecessary due to the OPEN status of the ticket",
                "[ BUSY ] Reading comment information...",
                "Found 3 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 3)...",
                "Transferred to ",
            ],
            id="Transferring particular issue tickets with OPEN status along with states and comments but without labels, without privacy and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --select 2 --commit --comments --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, with states, without privacy, with comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
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
            id="Transferring particular issue tickets with SHUT status along with states and comments but without labels, without privacy and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --select 1 --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
            ],
            id="Transferring particular issue tickets with OPEN status without labels, without states, without privacy, without comments and with order when SHUT status is prescribed",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --commit --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, with states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 4 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Assertion unnecessary due to the OPEN status of the ticket",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
                "[ BUSY ] Migrating issue ticket without labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
                "[ BUSY ] Migrating issue ticket without labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Asserting issue ticket status...",
                "Asserted CLOSE status of the ticket in ",
            ],
            id="Transferring issue tickets with FULL status along with states but without comments, without privacy, without labels and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --labels --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets with labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket with labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket with labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
            ],
            id="Transferring issue tickets with OPEN status along with labels but without states, without privacy, without comments and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --labels --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets with labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket with labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Migrating issue ticket with labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
            ],
            id="Transferring issue tickets with SHUT status along with labels but without states, without privacy, without comments and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --labels --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets with labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "Found 4 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket with labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Migrating issue ticket with labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Migrating issue ticket with labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Migrating issue ticket with labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with FULL status along with labels but without states, without privacy, without comments and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --comments --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states, without privacy, with comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Reading comment information...",
                "Found 3 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 3)...",
                "Transferred to ",
                "[ BUSY ] Migrating issue ticket without labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Reading comment information...",
                "Found 2 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 2)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 2)...",
                "Transferred to ",
            ],
            id="Transferring issue tickets with OPEN status along with comments but without labels, without privacy, without states and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --comments --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states, without privacy, with comments and with order off the given selection",  # noqa: E501
                "Found 2 issue ticket(s) across 1 page(s) in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
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
                "[ BUSY ] Migrating issue ticket without labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Reading comment information...",
                "Found 3 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 3)...",
                "Transferred to ",
            ],
            id="Transferring issue tickets with SHUT status along with comments but without labels, without privacy, without states and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --comments --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states, without privacy, with comments and with order off the given selection",  # noqa: E501
                "Found 4 issue ticket(s) across 1 page(s) in ",
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
                "[ BUSY ] Migrating issue ticket without labels #3 'This is the title of the third test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Reading comment information...",
                "Found 2 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 2)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 2)...",
                "Transferred to ",
                "[ BUSY ] Migrating issue ticket without labels #4 'This is the title of the fourth test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to ",
                "[ BUSY ] Reading comment information...",
                "Found 3 entities in ",
                "[ BUSY ] Transferring comment (Entity 1 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 2 of 3)...",
                "Transferred to ",
                "[ BUSY ] Transferring comment (Entity 3 of 3)...",
                "Transferred to ",
            ],
            id="Transferring issue tickets with FULL status along with comments but without labels, without privacy, without states and with order",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --ranges 1 2 --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
            ],
            id="Transferring issue tickets with OPEN status without labels, without states, without privacy, without comments and with order the identities of which fall in the given range",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --ranges 1 2 --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with SHUT status without labels, without states, without privacy, without comments and with order the identities of which fall in the given range",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --ranges 1 2 --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with FULL status without labels, without states, without privacy, without comments and with order the identities of which fall in the given range",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN --select 1,2 --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all open issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
            ],
            id="Transferring issue tickets with OPEN status without labels, without states, without privacy, without comments and with order the identities of which fall in the given selection",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status SHUT --select 1,2 --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all closed issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Skipping issue ticket as the issue ticket status does not match the provided status",  # noqa: E501
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with SHUT status without labels, without states, without privacy, without comments and with order the identities of which fall in the given selection",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status FULL --select 1,2 --series",  # noqa: E501
            0,
            [
                "[ WARN ] Extracting all issue tickets without labels, without states, without privacy, without comments and with order off the given selection",  # noqa: E501
                "[ BUSY ] Probing issue ticket #1...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #1 'This is the title of the first test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
                "[ BUSY ] Probing issue ticket #2...",
                "Information retrieved in ",
                "[ BUSY ] Migrating issue ticket without labels #2 'This is the title of the second test issue' by 'Akashdeep Dhar (ID t0xic0der)'...",  # noqa: E501
                "Migrated to",
            ],
            id="Transferring issue tickets with FULL status without labels, without states, without privacy, without comments and with order the identities of which fall in the given selection",  # noqa: E501
        ),
    ],
)
def test_main_tkts(wipe_issues, caplog, cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.issutnfs = 0
