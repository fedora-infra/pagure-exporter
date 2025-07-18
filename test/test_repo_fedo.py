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
from pagure_exporter.view.dcrt import conceal


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Available in source namespace: 8 branch(es)",
                "- (SRCE branch) HEAD",
                "- (SRCE branch) main",
                "- (SRCE branch) test-aaaa",
                "- (SRCE branch) test-bbbb",
                "- (SRCE branch) test-cccc",
                "- (SRCE branch) test-dddd",
                "- (SRCE branch) test-eeee",
                "- (SRCE branch) test-ffff",
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 8 available branches",
                "[1/8] Branch 'HEAD' was transferred to the destination namespace",
                "[2/8] Branch 'main' was transferred to the destination namespace",
                "[3/8] Branch 'test-aaaa' was transferred to the destination namespace",
                "[4/8] Branch 'test-bbbb' was transferred to the destination namespace",
                "[5/8] Branch 'test-cccc' was transferred to the destination namespace",
                "[6/8] Branch 'test-dddd' was transferred to the destination namespace",
                "[7/8] Branch 'test-eeee' was transferred to the destination namespace",
                "[8/8] Branch 'test-ffff' was transferred to the destination namespace",
                "Assets transferred: 8 branch(es) completed, 8 branch(es) requested",
                "[ PASS ] Namespace assets branch(es) transfer succeeded!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Available in source namespace: 0 tag(s)",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 0 available tags",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="pagure.io - Migrating repository contents with specifying zero valid branch and tag names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs test-aaaa,test-bbbb,test-cccc,test-dddd",  # noqa: E501
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
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'test-aaaa' was transferred to the destination namespace",
                "[2/4] Branch 'test-bbbb' was transferred to the destination namespace",
                "[3/4] Branch 'test-cccc' was transferred to the destination namespace",
                "[4/4] Branch 'test-dddd' was transferred to the destination namespace",
                "Assets transferred: 4 branch(es) completed, 4 branch(es) requested",
                "[ PASS ] Namespace assets branch(es) transfer succeeded!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Available in source namespace: 0 tag(s)",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 0 available tags",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="pagure.io - Migrating repository contents with specifying four valid branch names and zero valid tag names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs test-aaaa,test-bbbb,test-cxxc,test-dxxd",  # noqa: E501
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
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'test-aaaa' was transferred to the destination namespace",
                "[2/4] Branch 'test-bbbb' was transferred to the destination namespace",
                "[3/4] Branch 'test-cxxc' was not found in the source namespace",
                "[4/4] Branch 'test-dxxd' was not found in the source namespace",
                "Assets transferred: 2 branch(es) completed, 4 branch(es) requested",
                "[ WARN ] Namespace assets branch(es) transfer partially completed!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Available in source namespace: 0 tag(s)",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 0 available tags",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="pagure.io - Migrating repository contents with specifying two valid branch names and two invalid branch names and zero valid tag names",  # noqa: E501
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs test-axxa,test-bxxb,test-cxxc,test-dxxd",  # noqa: E501
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
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'test-axxa' was not found in the source namespace",
                "[2/4] Branch 'test-bxxb' was not found in the source namespace",
                "[3/4] Branch 'test-cxxc' was not found in the source namespace",
                "[4/4] Branch 'test-dxxd' was not found in the source namespace",
                "Assets transferred: 0 branch(es) completed, 4 branch(es) requested",
                "[ FAIL ] Namespace assets branch(es) transfer failed!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Available in source namespace: 0 tag(s)",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 0 available tags",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="pagure.io - Migrating repository contents with specifying four invalid branch names and zero invalid tag names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                f"Address: https://{envr['TEST_FUSR']}:{conceal(envr['TEST_PKEY'])}@{envr['TEST_SPLT_FEDO']}/{envr['TEST_SRCE']}.git",  # noqa: E501
            ],
            id="pagure.io - Checking the correctness of metadata censorship for source namespace",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                f"Address: https://{envr['TEST_TUSR']}:{conceal(envr['TEST_GKEY'])}@{envr['TEST_DPLT']}/{envr['TEST_TUSR']}",  # noqa: E501
            ],
            id="pagure.io - Checking the correctness of metadata censorship for destination namespace",
        ),
    ],
)
def test_main_repo(caplog, cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.branch_transfer_index = 0
    standard.tag_transfer_index = 0

    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
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
            id="pagure.io - Cloning repository contents of the source namespace into an inoperable location",
        ),
    ],
)
def test_push_repo(caplog, cmdl, code, text):
    # Setting the temporary directory creation location to where the current user does not have
    # appropriate permissions to operate on to intentionally invoke an error
    standard.temp_dir = "/etc"

    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.temp_dir = "/var/tmp"  # noqa: S108

    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101
