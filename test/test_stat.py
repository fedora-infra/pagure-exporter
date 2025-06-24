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

from pagure_exporter.main import main


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"], allow_playback_repeats=True, match_on=["method", "scheme", "host", "port", "query"])
@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            f"--splt {envr['TEST_SPLT_FEDO']} --dplt {envr['TEST_DPLT']} --srce {envr['TEST_SRCE']} --dest {envr['TEST_DEST']} --pkey {envr['TEST_PKEY']} --gkey STUPIDCODE --fusr {envr['TEST_FUSR']} --tusr {envr['TEST_TUSR']} tkts --status OPEN",  # noqa: E501
            1,
            [
                "Destination namespace metadata acquisition failed!",
                "The namespace metadata could not be acquired.",
                "Code: 0",
                "Reason: 401: 401 Unauthorized",
            ],
            id="Checking for possible errors while attempting to authenticate in the destination namespace using wrong credentials",  # noqa: E501
        ),
    ],
)
def test_stat_destdata_obtninfo(caplog, cmdl, code, text):
    runner = CliRunner()
    result = runner.invoke(main, cmdl)
    assert result.exit_code == code  # noqa: S101
    for indx in text:
        assert indx in caplog.text  # noqa: S101
