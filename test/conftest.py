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


from os import environ as envr

import pytest
from gitlab import Gitlab
from requests import Session

from pagure_exporter.conf import standard


def wipe_cookies():
    def before_record_response(response):
        response["headers"]["Set-Cookie"] = ""
        return response
    return before_record_response


def pytest_recording_configure(config, vcr):
    vcr.before_record_response = wipe_cookies()


@pytest.fixture(scope="function")
def wipe_issues():
    """
    Clean all existing issue tickets before running the issue creation related tests
    """

    gobj = Gitlab(
        url="https://gitlab.com",
        private_token=envr['TEST_GKEY'],
        timeout=30,
        retry_transient_errors=True,
        session=Session()
    )
    gpro = gobj.projects.get(id=envr["TEST_DEST"])

    # There are a maximum of 4 issue tickets at https://pagure.io/protop2g-test-srce/issues
    # Change this variable if the issue tickets are created or deleted from there
    qant = 4

    for indx in range(1, qant+1):
        try:
            gpro.issues.delete(str(indx))
            standard.logger.info(f"Issue #{indx} was deleted")
        except Exception as expt:
            standard.logger.info(f"Issue #{indx} could not be deleted due to {expt}")
