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
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "Branch 'HEAD' was transferred to the destination namespace",
                "Branch 'c10s-sig-hyperscale' was transferred to the destination namespace",
                "Branch 'c10s-sig-hyperscale-v255' was transferred to the destination namespace",
                "Branch 'c4' was transferred to the destination namespace",
                "Branch 'c5' was transferred to the destination namespace",
                "Branch 'c5-plus' was transferred to the destination namespace",
                "Branch 'c6' was transferred to the destination namespace",
                "Branch 'c6-plus' was transferred to the destination namespace",
                "Branch 'c7' was transferred to the destination namespace",
                "Branch 'c7-alt' was transferred to the destination namespace",
                "Branch 'c7-atomic' was transferred to the destination namespace",
                "Branch 'c7-atomic-beta' was transferred to the destination namespace",
                "Branch 'c7-beta' was transferred to the destination namespace",
                "Branch 'c7-sig-altarch-fasttrack' was transferred to the destination namespace",
                "Branch 'c8' was transferred to the destination namespace",
                "Branch 'c8-beta' was transferred to the destination namespace",
                "Branch 'c8s' was transferred to the destination namespace",
                "Branch 'c8s-sig-hyperscale' was transferred to the destination namespace",
                "Branch 'c9' was transferred to the destination namespace",
                "Branch 'c9-beta' was transferred to the destination namespace",
                "Branch 'c9s-sig-hyperscale' was transferred to the destination namespace",
                "Branch 'c9s-sig-hyperscale-v255' was transferred to the destination namespace",
                "[ PASS ] Namespace assets branch(es) transfer succeeded!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Available in source namespace:",
                "- (SRCE tag) imports/c9-beta/systemd-249-7.el9_b",
                "- (SRCE tag) imports/c9-beta/systemd-249-9.el9",
                "- (SRCE tag) imports/c9-beta/systemd-250-11.el9",
                "- (SRCE tag) imports/c9-beta/systemd-250-3.el9",
                "- (SRCE tag) imports/c9-beta/systemd-250-4.el9",
                "- (SRCE tag) imports/c9-beta/systemd-252-8.el9",
                "- (SRCE tag) imports/c9/systemd-250-12.el9_1",
                "- (SRCE tag) imports/c9/systemd-250-12.el9_1.1",
                "- (SRCE tag) imports/c9/systemd-250-12.el9_1.3",
                "- (SRCE tag) imports/c9/systemd-250-6.el9_0",
                "- (SRCE tag) imports/c9/systemd-250-6.el9_0.1",
                "- (SRCE tag) imports/c9/systemd-252-13.el9_2",
                "Requested for transferring: 0 tag(s)",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "Tag 'imports/c9-beta/systemd-249-7.el9_b' was transferred to the destination namespace",
                "Tag 'imports/c9-beta/systemd-249-9.el9' was transferred to the destination namespace",
                "Tag 'imports/c9-beta/systemd-250-11.el9' was transferred to the destination namespace",
                "Tag 'imports/c9-beta/systemd-250-3.el9' was transferred to the destination namespace",
                "Tag 'imports/c9-beta/systemd-250-4.el9' was transferred to the destination namespace",
                "Tag 'imports/c9-beta/systemd-252-8.el9' was transferred to the destination namespace",
                "Tag 'imports/c9/systemd-250-12.el9_1' was transferred to the destination namespace",
                "Tag 'imports/c9/systemd-250-12.el9_1.1' was transferred to the destination namespace",
                "Tag 'imports/c9/systemd-250-12.el9_1.3' was transferred to the destination namespace",
                "Tag 'imports/c9/systemd-250-6.el9_0' was transferred to the destination namespace",
                "Tag 'imports/c9/systemd-250-6.el9_0.1' was transferred to the destination namespace",
                "Tag 'imports/c9/systemd-252-13.el9_2' was transferred to the destination namespace",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="git.centos.org - Migrating repository contents with specifying zero valid branch and tag names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs c10s-sig-hyperscale,c10s-sig-hyperscale-v255,c9s-sig-hyperscale,c9s-sig-hyperscale-v255 --tags imports/c9/systemd-250-12.el9_1.3,imports/c9/systemd-250-6.el9_0,imports/c9/systemd-250-6.el9_0.1,imports/c9/systemd-252-13.el9_2",  # noqa: E501
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
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'c10s-sig-hyperscale' was transferred to the destination namespace",
                "[2/4] Branch 'c10s-sig-hyperscale-v255' was transferred to the destination namespace",
                "[3/4] Branch 'c9s-sig-hyperscale' was transferred to the destination namespace",
                "[4/4] Branch 'c9s-sig-hyperscale-v255' was transferred to the destination namespace",
                "Assets transferred: 4 branch(es) completed, 4 branch(es) requested",
                "[ PASS ] Namespace assets branch(es) transfer succeeded!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Requested for transferring: 4 tag(s)",
                "- (RQST tag) imports/c9/systemd-250-12.el9_1.3",
                "- (RQST tag) imports/c9/systemd-250-6.el9_0",
                "- (RQST tag) imports/c9/systemd-250-6.el9_0.1",
                "- (RQST tag) imports/c9/systemd-252-13.el9_2",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 4 requested tags",
                "[1/4] Tag 'imports/c9/systemd-250-12.el9_1.3' was transferred to the destination namespace",
                "[2/4] Tag 'imports/c9/systemd-250-6.el9_0' was transferred to the destination namespace",
                "[3/4] Tag 'imports/c9/systemd-250-6.el9_0.1' was transferred to the destination namespace",
                "[4/4] Tag 'imports/c9/systemd-252-13.el9_2' was transferred to the destination namespace",
                "Assets transferred: 4 tag(s) completed, 4 tag(s) requested",
                "[ PASS ] Namespace assets tag(s) transfer succeeded!",
            ],
            id="git.centos.org - Migrating repository contents with specifying four valid branch and tag names",
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs c10s-sig-hyperscale,c10s-sig-hyperscale-v255,c90s-sig-hyperscale,c90s-sig-hyperscale-v255 --tags imports/c9/systemd-250-12.el9_1.3,imports/c9/systemd-250-6.el9_0,imports/c90/systemd-250-6.el9_0.1,imports/c90/systemd-252-13.el9_2",  # noqa: E501
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
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'c10s-sig-hyperscale' was transferred to the destination namespace",
                "[2/4] Branch 'c10s-sig-hyperscale-v255' was transferred to the destination namespace",
                "[3/4] Branch 'c90s-sig-hyperscale' was not found in the source namespace",
                "[4/4] Branch 'c90s-sig-hyperscale-v255' was not found in the source namespace",
                "Assets transferred: 2 branch(es) completed, 4 branch(es) requested",
                "[ WARN ] Namespace assets branch(es) transfer partially completed!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Requested for transferring: 4 tag(s)",
                "- (RQST tag) imports/c9/systemd-250-12.el9_1.3",
                "- (RQST tag) imports/c9/systemd-250-6.el9_0",
                "- (RQST tag) imports/c90/systemd-250-6.el9_0.1",
                "- (RQST tag) imports/c90/systemd-252-13.el9_2",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 4 requested tags",
                "[1/4] Tag 'imports/c9/systemd-250-12.el9_1.3' was transferred to the destination namespace",
                "[2/4] Tag 'imports/c9/systemd-250-6.el9_0' was transferred to the destination namespace",
                "[3/4] Tag 'imports/c90/systemd-250-6.el9_0.1' was not found in the source namespace",
                "[4/4] Tag 'imports/c90/systemd-252-13.el9_2' was not found in the source namespace",
                "Assets transferred: 2 tag(s) completed, 4 tag(s) requested",
                "[ WARN ] Namespace assets tag(s) transfer partially completed!",
            ],
            id="git.centos.org - Migrating repository contents with specifying two valid branch and tag names and two invalid branch and tag names",  # noqa: E501
        ),
        pytest.param(
            f"--splt {envr['TEST_SPLT_CENT']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE_CENT']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY_CENT']} --gkey {envr['TEST_GKEY']} --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} repo --brcs c10s-sig-hypersonic,c10s-sig-hypersonic-v255,c9s-sig-hypersonic,c9s-sig-hypersonic-v255 --tags imports/c90/systemd-250-12.el9_1.3,imports/c90/systemd-250-6.el9_0,imports/c90/systemd-250-6.el9_0.1,imports/c90/systemd-252-13.el9_2",  # noqa: E501
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
                "[ BUSY ] Initializing namespace assets branch(es) transfer...",
                "[ WARN ] Transferring 4 requested branches",
                "[1/4] Branch 'c10s-sig-hypersonic' was not found in the source namespace",
                "[2/4] Branch 'c10s-sig-hypersonic-v255' was not found in the source namespace",
                "[3/4] Branch 'c9s-sig-hypersonic' was not found in the source namespace",
                "[4/4] Branch 'c9s-sig-hypersonic-v255' was not found in the source namespace",
                "Assets transferred: 0 branch(es) completed, 4 branch(es) requested",
                "[ FAIL ] Namespace assets branch(es) transfer failed!",
                "[ BUSY ] Reading tags data from the locally cloned assets...",
                "[ PASS ] Tags data reading succeeded!",
                "Requested for transferring: 4 tag(s)",
                "- (RQST tag) imports/c90/systemd-250-12.el9_1.3",
                "- (RQST tag) imports/c90/systemd-250-6.el9_0",
                "- (RQST tag) imports/c90/systemd-250-6.el9_0.1",
                "- (RQST tag) imports/c90/systemd-252-13.el9_2",
                "[ BUSY ] Initializing namespace assets tag(s) transfer...",
                "[ WARN ] Transferring 4 requested tags",
                "[1/4] Tag 'imports/c90/systemd-250-12.el9_1.3' was not found in the source namespace",
                "[2/4] Tag 'imports/c90/systemd-250-6.el9_0' was not found in the source namespace",
                "[3/4] Tag 'imports/c90/systemd-250-6.el9_0.1' was not found in the source namespace",
                "[4/4] Tag 'imports/c90/systemd-252-13.el9_2' was not found in the source namespace",
                "Assets transferred: 0 tag(s) completed, 4 tag(s) requested",
                "[ FAIL ] Namespace assets tag(s) transfer failed!",
            ],
            id="git.centos.org - Migrating repository contents with specifying four invalid branch and tag names",
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
    standard.branch_transfer_index = 0
    standard.tag_transfer_index = 0

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
