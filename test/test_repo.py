"""
Pagure Exporter
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

from pagure_exporter.conf import standard
from pagure_exporter.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Available in source namespace: 6 branch(es)",
                "- (SRCE branch) HEAD",
                "- (SRCE branch) main",
                "- (SRCE branch) test-aaaa",
                "- (SRCE branch) test-bbbb",
                "- (SRCE branch) test-cccc",
                "- (SRCE branch) test-dddd",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 6 available branches",
                "[1/6] Branch 'HEAD' was transferred to the destination namespace",
                "[2/6] Branch 'main' was transferred to the destination namespace",
                "[3/6] Branch 'test-aaaa' was transferred to the destination namespace",
                "[4/6] Branch 'test-bbbb' was transferred to the destination namespace",
                "[5/6] Branch 'test-cccc' was transferred to the destination namespace",
                "[6/6] Branch 'test-dddd' was transferred to the destination namespace",
                "Assets transferred: 6 branch(es) completed, 6 branch(es) requested",
                "[ PASS ] Namespace assets transfer succeeded!",
            ],
            id="Migrating repository contents with specifying zero valid branch names",
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs test-aaaa,test-bbbb,test-cccc,test-dddd",  # noqa: E501
            0,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) test-aaaa",
                "- (RQST branch) test-bbbb",
                "- (RQST branch) test-cccc",
                "- (RQST branch) test-dddd",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'test-aaaa' was transferred to the destination namespace",
                "[2/4] Branch 'test-bbbb' was transferred to the destination namespace",
                "[3/4] Branch 'test-cccc' was transferred to the destination namespace",
                "[4/4] Branch 'test-dddd' was transferred to the destination namespace",
                "Assets transferred: 4 branch(es) completed, 4 branch(es) requested",
                "[ PASS ] Namespace assets transfer succeeded!",
            ],
            id="Migrating repository contents with specifying four valid branch names",
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs test-aaaa,test-bbbb,test-cxxc,test-dxxd",  # noqa: E501
            2,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) test-aaaa",
                "- (RQST branch) test-bbbb",
                "- (RQST branch) test-cxxc",
                "- (RQST branch) test-dxxd",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'test-aaaa' was transferred to the destination namespace",
                "[2/4] Branch 'test-bbbb' was transferred to the destination namespace",
                "[3/4] Branch 'test-cxxc' was not found in the source namespace",
                "[4/4] Branch 'test-dxxd' was not found in the source namespace",
                "Assets transferred: 2 branch(es) completed, 4 branch(es) requested",
                "[ WARN ] Namespace assets transfer partially completed!",
            ],
            id="Migrating repository contents with specifying two valid branch names and two invalid branch names",  # noqa: E501
        ),
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs test-axxa,test-bxxb,test-cxxc,test-dxxd",  # noqa: E501
            1,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) test-axxa",
                "- (RQST branch) test-bxxb",
                "- (RQST branch) test-cxxc",
                "- (RQST branch) test-dxxd",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'test-axxa' was not found in the source namespace",
                "[2/4] Branch 'test-bxxb' was not found in the source namespace",
                "[3/4] Branch 'test-cxxc' was not found in the source namespace",
                "[4/4] Branch 'test-dxxd' was not found in the source namespace",
                "Assets transferred: 0 branch(es) completed, 4 branch(es) requested",
                "[ FAIL ] Namespace assets transfer failed!",
            ],
            id="Migrating repository contents with specifying four invalid branch names",
        ),
    ],
)
def test_main_repo(caplog, cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.tnfsindx = 0

    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            1,
            [
                "[ BUSY ] Requesting for source namespace metadata...",
                "[ PASS ] Source namespace metadata acquisition succeeded!",
                "[ BUSY ] Requesting for destination namespace metadata...",
                "[ PASS ] Destination namespace metadata acquisition succeeded!",
                "[ BUSY ] Starting migration...",
                "[ FAIL ] Migration failed!",
                "Exception occurred: [Errno 13] Permission denied: ",
            ],
            id="Cloning repository contents of the source namespace into an inoperable location",
        ),
    ],
)
def test_push_repo(caplog, cmdl, code, text):
    # Setting the temporary directory creation location to where the current user does not have
    # appropriate permissions to operate on to intentionally invoke an error
    standard.tempdrct = "/etc"

    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.tempdrct = "/var/tmp"  # noqa: S108

    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101
