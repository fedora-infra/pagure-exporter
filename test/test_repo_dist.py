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
            f"--splt {envr['TEST_SPLT_DIST']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_DIST']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_DIST']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
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
                "- (SRCE branch) f14",
                "- (SRCE branch) f15",
                "- (SRCE branch) f16",
                "- (SRCE branch) f17",
                "- (SRCE branch) f18",
                "- (SRCE branch) f19",
                "- (SRCE branch) f20",
                "- (SRCE branch) f21",
                "- (SRCE branch) f22",
                "- (SRCE branch) f23",
                "- (SRCE branch) f24",
                "- (SRCE branch) f25",
                "- (SRCE branch) f26",
                "- (SRCE branch) f27",
                "- (SRCE branch) f28",
                "- (SRCE branch) f29",
                "- (SRCE branch) f30",
                "- (SRCE branch) f31",
                "- (SRCE branch) f32",
                "- (SRCE branch) f33",
                "- (SRCE branch) f34",
                "- (SRCE branch) f35",
                "- (SRCE branch) f36",
                "- (SRCE branch) f37",
                "- (SRCE branch) f38",
                "- (SRCE branch) f39",
                "- (SRCE branch) f40",
                "- (SRCE branch) f41",
                "- (SRCE branch) f42",
                "- (SRCE branch) main",
                "- (SRCE branch) rawhide",
                "- (SRCE branch) rhughes/chassis-type-backport",
                "- (SRCE branch) rpm-master",
                "Requested for transferring: 0 branch(es)",
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 34 available branches",
                "Branch 'HEAD' was transferred to the destination namespace",
                "Branch 'f14' was transferred to the destination namespace",
                "Branch 'f15' was transferred to the destination namespace",
                "Branch 'f16' was transferred to the destination namespace",
                "Branch 'f17' was transferred to the destination namespace",
                "Branch 'f18' was transferred to the destination namespace",
                "Branch 'f19' was transferred to the destination namespace",
                "Branch 'f20' was transferred to the destination namespace",
                "Branch 'f21' was transferred to the destination namespace",
                "Branch 'f22' was transferred to the destination namespace",
                "Branch 'f23' was transferred to the destination namespace",
                "Branch 'f24' was transferred to the destination namespace",
                "Branch 'f25' was transferred to the destination namespace",
                "Branch 'f26' was transferred to the destination namespace",
                "Branch 'f27' was transferred to the destination namespace",
                "Branch 'f28' was transferred to the destination namespace",
                "Branch 'f29' was transferred to the destination namespace",
                "Branch 'f30' was transferred to the destination namespace",
                "Branch 'f31' was transferred to the destination namespace",
                "Branch 'f32' was transferred to the destination namespace",
                "Branch 'f33' was transferred to the destination namespace",
                "Branch 'f34' was transferred to the destination namespace",
                "Branch 'f35' was transferred to the destination namespace",
                "Branch 'f36' was transferred to the destination namespace",
                "Branch 'f37' was transferred to the destination namespace",
                "Branch 'f38' was transferred to the destination namespace",
                "Branch 'f39' was transferred to the destination namespace",
                "Branch 'f40' was transferred to the destination namespace",
                "Branch 'f41' was transferred to the destination namespace",
                "Branch 'f42' was transferred to the destination namespace",
                "Branch 'main' was transferred to the destination namespace",
                "Branch 'rawhide' was transferred to the destination namespace",
                "Branch 'rhughes/chassis-type-backport' was transferred to the destination namespace",
                "Branch 'rpm-master' was transferred to the destination namespace",
                "[ PASS ] Namespace assets branch(es) transfer succeeded!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Available in source namespace:",
                "- (SRCE tag) systemd-217-1.fc22",
                "- (SRCE tag) systemd-217-2.fc22",
                "- (SRCE tag) systemd-217-3.fc22",
                "- (SRCE tag) systemd-217-4.fc22",
                "- (SRCE tag) systemd-3-1_fc14",
                "- (SRCE tag) systemd-3-2_fc14",
                "- (SRCE tag) systemd-3-3_fc14",
                "- (SRCE tag) systemd-4-1_fc14",
                "- (SRCE tag) systemd-4-2_fc14",
                "- (SRCE tag) systemd-4-3_fc14",
                "- (SRCE tag) systemd-4-4_fc14",
                "Requested for transferring: 0 tag(s)",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "Tag 'systemd-217-1.fc22' was transferred to the destination namespace",
                "Tag 'systemd-217-2.fc22' was transferred to the destination namespace",
                "Tag 'systemd-217-3.fc22' was transferred to the destination namespace",
                "Tag 'systemd-217-4.fc22' was transferred to the destination namespace",
                "Tag 'systemd-3-1_fc14' was transferred to the destination namespace",
                "Tag 'systemd-3-2_fc14' was transferred to the destination namespace",
                "Tag 'systemd-3-3_fc14' was transferred to the destination namespace",
                "Tag 'systemd-4-1_fc14' was transferred to the destination namespace",
                "Tag 'systemd-4-2_fc14' was transferred to the destination namespace",
                "Tag 'systemd-4-3_fc14' was transferred to the destination namespace",
                "Tag 'systemd-4-4_fc14' was transferred to the destination namespace",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="src.fedoraproject.org - Migrating repository contents with specifying zero valid branch and tag names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_DIST']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_DIST']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_DIST']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs rawhide,f42,f41,f40 --tags systemd-4-1_fc14,systemd-4-2_fc14,systemd-4-3_fc14,systemd-4-4_fc14",  # noqa: E501
            0,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) rawhide",
                "- (RQST branch) f42",
                "- (RQST branch) f41",
                "- (RQST branch) f40",
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'rawhide' was transferred to the destination namespace",
                "[2/4] Branch 'f42' was transferred to the destination namespace",
                "[3/4] Branch 'f41' was transferred to the destination namespace",
                "[4/4] Branch 'f40' was transferred to the destination namespace",
                "Assets transferred: 4 branch(es) completed, 4 branch(es) requested",
                "[ PASS ] Namespace assets branch(es) transfer succeeded!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Requested for transferring: 4 tag(s)",
                "- (RQST tag) systemd-4-1_fc14",
                "- (RQST tag) systemd-4-2_fc14",
                "- (RQST tag) systemd-4-3_fc14",
                "- (RQST tag) systemd-4-4_fc14",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 4 requested tags",
                "[1/4] Tag 'systemd-4-1_fc14' was transferred to the destination namespace",
                "[2/4] Tag 'systemd-4-2_fc14' was transferred to the destination namespace",
                "[3/4] Tag 'systemd-4-3_fc14' was transferred to the destination namespace",
                "[4/4] Tag 'systemd-4-4_fc14' was transferred to the destination namespace",
                "Assets transferred: 4 tag(s) completed, 4 tag(s) requested",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="src.fedoraproject.org - Migrating repository contents with specifying four valid branch names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_DIST']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_DIST']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_DIST']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs rawhide,f42,fast,furious --tags systemd-4-1_fc14,systemd-4-2_fc14,systemd-5-3_fc14,systemd-5-4_fc14",  # noqa: E501
            2,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) rawhide",
                "- (RQST branch) f42",
                "- (RQST branch) fast",
                "- (RQST branch) furious",
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'rawhide' was transferred to the destination namespace",
                "[2/4] Branch 'f42' was transferred to the destination namespace",
                "[3/4] Branch 'fast' was not found in the source namespace",
                "[4/4] Branch 'furious' was not found in the source namespace",
                "Assets transferred: 2 branch(es) completed, 4 branch(es) requested",
                "[ WARN ] Namespace assets branch(es) transfer partially completed!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Requested for transferring: 4 tag(s)",
                "- (RQST tag) systemd-4-1_fc14",
                "- (RQST tag) systemd-4-2_fc14",
                "- (RQST tag) systemd-5-3_fc14",
                "- (RQST tag) systemd-5-4_fc14",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 4 requested tags",
                "[1/4] Tag 'systemd-4-1_fc14' was transferred to the destination namespace",
                "[2/4] Tag 'systemd-4-2_fc14' was transferred to the destination namespace",
                "[3/4] Tag 'systemd-5-3_fc14' was not found in the source namespace",
                "[4/4] Tag 'systemd-5-4_fc14' was not found in the source namespace",
                "Assets transferred: 2 tag(s) completed, 4 tag(s) requested",
                "[ WARN ] Namespace assets tag(s) transfer partially completed!",
            ],
            id="src.fedoraproject.org - Migrating repository contents with specifying two valid branch and tag names and two invalid branch and tag names",  # noqa: E501
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_DIST']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_DIST']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_DIST']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs faulty-rawhide,faulty-f42,faulty-f41,faulty-f40 --tags systemd-5-1_fc14,systemd-5-2_fc14,systemd-5-3_fc14,systemd-5-4_fc14",  # noqa: E501
            1,
            [
                "[ BUSY ] Attempting source namespace assets clone...",
                "[ PASS ] Source namespace assets clone succeeded!",
                "[ BUSY ] Attempting destination namespace assets clone...",
                "[ PASS ] Destination namespace assets clone succeeded!",
                "[ BUSY ] Reading branches data from the locally cloned assets...",
                "[ PASS ] Branches data reading succeeded!",
                "Requested for transferring: 4 branch(es)",
                "- (RQST branch) faulty-rawhide",
                "- (RQST branch) faulty-f42",
                "- (RQST branch) faulty-f41",
                "- (RQST branch) faulty-f40",
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'faulty-rawhide' was not found in the source namespace",
                "[2/4] Branch 'faulty-f42' was not found in the source namespace",
                "[3/4] Branch 'faulty-f41' was not found in the source namespace",
                "[4/4] Branch 'faulty-f40' was not found in the source namespace",
                "Assets transferred: 0 branch(es) completed, 4 branch(es) requested",
                "[ FAIL ] Namespace assets branch(es) transfer failed!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Requested for transferring: 4 tag(s)",
                "- (RQST tag) systemd-5-1_fc14",
                "- (RQST tag) systemd-5-2_fc14",
                "- (RQST tag) systemd-5-3_fc14",
                "- (RQST tag) systemd-5-4_fc14",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 4 requested tags",
                "[1/4] Tag 'systemd-5-1_fc14' was not found in the source namespace",
                "[2/4] Tag 'systemd-5-2_fc14' was not found in the source namespace",
                "[3/4] Tag 'systemd-5-3_fc14' was not found in the source namespace",
                "[4/4] Tag 'systemd-5-4_fc14' was not found in the source namespace",
                "Assets transferred: 0 tag(s) completed, 4 tag(s) requested",
                "[ FAIL ] Namespace assets tag(s) transfer failed!",
            ],
            id="src.fedoraproject.org - Migrating repository contents with specifying four invalid branch names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_DIST']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_DIST']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_DIST']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                f"Address: https://{envr['TEST_FUSR']}:{conceal(envr['TEST_PKEY_DIST'])}@{envr['TEST_SPLT_DIST']}/{envr['TEST_SRCE_DIST']}.git",  # noqa: E501
            ],
            id="src.fedoraproject.org - Checking the correctness of metadata censorship for source namespace",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_DIST']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_DIST']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_DIST']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
            0,
            [
                f"Address: https://{envr['TEST_TUSR']}:{conceal(envr['TEST_GKEY'])}@{envr['TEST_DPLT']}/{envr['TEST_TUSR']}",  # noqa: E501
            ],
            id="src.fedoraproject.org - Checking the correctness of metadata censorship for destination namespace",
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
            f"--splt {envr['TEST_SPLT_DIST']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_DIST']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_DIST']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo",  # noqa: E501
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
            id="src.fedoraproject.org - Cloning repository contents of the source namespace into an inoperable location",
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
