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
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Available in source namespace:",
                "- (SRCE branch) HEAD",
                "- (SRCE branch) c10s-sig-hyperscale",
                "- (SRCE branch) c10s-sig-hyperscale-v255",
                "- (SRCE branch) c4",
                "- (SRCE branch) c5",
                "- (SRCE branch) c5-plus",
                "- (SRCE branch) c6",
                "- (SRCE branch) c6-plus",
                "- (SRCE branch) c7",
                "- (SRCE branch) c7-alt",
                "- (SRCE branch) c7-atomic",
                "- (SRCE branch) c7-atomic-beta",
                "- (SRCE branch) c7-beta",
                "- (SRCE branch) c7-sig-altarch-fasttrack",
                "- (SRCE branch) c8",
                "- (SRCE branch) c8-beta",
                "- (SRCE branch) c8s",
                "- (SRCE branch) c8s-sig-hyperscale",
                "- (SRCE branch) c9",
                "- (SRCE branch) c9-beta",
                "- (SRCE branch) c9s-sig-hyperscale",
                "- (SRCE branch) c9s-sig-hyperscale-v255",
                "Requested for transferring: 0 branch(es)",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 22 available branches",
                "[1/22] Branch 'HEAD' was transferred to the destination namespace",
                "[2/22] Branch 'c10s-sig-hyperscale' was transferred to the destination namespace",
                "[3/22] Branch 'c10s-sig-hyperscale-v255' was transferred to the destination namespace",
                "[4/22] Branch 'c4' was transferred to the destination namespace",
                "[5/22] Branch 'c5' was transferred to the destination namespace",
                "[6/22] Branch 'c5-plus' was transferred to the destination namespace",
                "[7/22] Branch 'c6' was transferred to the destination namespace",
                "[8/22] Branch 'c6-plus' was transferred to the destination namespace",
                "[9/22] Branch 'c7' was transferred to the destination namespace",
                "[10/22] Branch 'c7-alt' was transferred to the destination namespace",
                "[11/22] Branch 'c7-atomic' was transferred to the destination namespace",
                "[12/22] Branch 'c7-atomic-beta' was transferred to the destination namespace",
                "[13/22] Branch 'c7-beta' was transferred to the destination namespace",
                "[14/22] Branch 'c7-sig-altarch-fasttrack' was transferred to the destination namespace",
                "[15/22] Branch 'c8' was transferred to the destination namespace",
                "[16/22] Branch 'c8-beta' was transferred to the destination namespace",
                "[17/22] Branch 'c8s' was transferred to the destination namespace",
                "[18/22] Branch 'c8s-sig-hyperscale' was transferred to the destination namespace",
                "[19/22] Branch 'c9' was transferred to the destination namespace",
                "[20/22] Branch 'c9-beta' was transferred to the destination namespace",
                "[21/22] Branch 'c9s-sig-hyperscale' was transferred to the destination namespace",
                "[22/22] Branch 'c9s-sig-hyperscale-v255' was transferred to the destination namespace",
                "Assets transferred: 22 branch(es) completed, 22 branch(es) requested",
                "[ PASS ] Namespace assets transfer succeeded!",
            ],
            id="git.centos.org - Migrating repository contents with specifying zero valid branch names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs c10s-sig-hyperscale,c10s-sig-hyperscale-v255,c9s-sig-hyperscale,c9s-sig-hyperscale-v255",  # noqa: E501
            0,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) c10s-sig-hyperscale",
                "- (RQST branch) c10s-sig-hyperscale-v255",
                "- (RQST branch) c9s-sig-hyperscale",
                "- (RQST branch) c9s-sig-hyperscale-v255",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'c10s-sig-hyperscale' was transferred to the destination namespace",
                "[2/4] Branch 'c10s-sig-hyperscale-v255' was transferred to the destination namespace",
                "[3/4] Branch 'c9s-sig-hyperscale' was transferred to the destination namespace",
                "[4/4] Branch 'c9s-sig-hyperscale-v255' was transferred to the destination namespace",
                "Assets transferred: 4 branch(es) completed, 4 branch(es) requested",
                "[ PASS ] Namespace assets transfer succeeded!",
            ],
            id="git.centos.org - Migrating repository contents with specifying four valid branch names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs c10s-sig-hyperscale,c10s-sig-hyperscale-v255,c90s-sig-hyperscale,c90s-sig-hyperscale-v255",  # noqa: E501
            2,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) c10s-sig-hyperscale",
                "- (RQST branch) c10s-sig-hyperscale-v255",
                "- (RQST branch) c90s-sig-hyperscale",
                "- (RQST branch) c90s-sig-hyperscale-v255",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'c10s-sig-hyperscale' was transferred to the destination namespace",
                "[2/4] Branch 'c10s-sig-hyperscale-v255' was transferred to the destination namespace",
                "[3/4] Branch 'c90s-sig-hyperscale' was not found in the source namespace",
                "[4/4] Branch 'c90s-sig-hyperscale-v255' was not found in the source namespace",
                "Assets transferred: 2 branch(es) completed, 4 branch(es) requested",
                "[ WARN ] Namespace assets transfer partially completed!",
            ],
            id="git.centos.org - Migrating repository contents with specifying two valid branch names and two invalid branch names",  # noqa: E501
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs c10s-sig-hypersonic,c10s-sig-hypersonic-v255,c9s-sig-hypersonic,c9s-sig-hypersonic-v255",  # noqa: E501
            1,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) c10s-sig-hypersonic",
                "- (RQST branch) c10s-sig-hypersonic-v255",
                "- (RQST branch) c9s-sig-hypersonic",
                "- (RQST branch) c9s-sig-hypersonic-v255",
                "[ BUSY ] Initializing namespace assets transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'c10s-sig-hypersonic' was not found in the source namespace",
                "[2/4] Branch 'c10s-sig-hypersonic-v255' was not found in the source namespace",
                "[3/4] Branch 'c9s-sig-hypersonic' was not found in the source namespace",
                "[4/4] Branch 'c9s-sig-hypersonic-v255' was not found in the source namespace",
                "Assets transferred: 0 branch(es) completed, 4 branch(es) requested",
                "[ FAIL ] Namespace assets transfer failed!",
            ],
            id="git.centos.org - Migrating repository contents with specifying four invalid branch names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                f"Address: https://{envr['TEST_FUSR']}:{conceal(envr['TEST_PKEY_CENT'])}@{envr['TEST_SPLT_CENT']}/{envr['TEST_SRCE_CENT']}.git",  # noqa: E501
            ],
            id="git.centos.org - Checking the correctness of metadata censorship for source namespace",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                f"Address: https://{envr['TEST_TUSR']}:{conceal(envr['TEST_GKEY'])}@{envr['TEST_DPLT']}/{envr['TEST_TUSR']}",  # noqa: E501
            ],
            id="git.centos.org - Checking the correctness of metadata censorship for destination namespace",
        ),
    ],
)
def test_main_repo(caplog, cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.transfer_index = 0

    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
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
            id="git.centos.org - Cloning repository contents of the source namespace into an inoperable location",
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
