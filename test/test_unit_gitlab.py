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


from datetime import datetime, timezone
from os import environ as envr
from time import time
from unittest.mock import Mock

import pytest
from gitlab.exceptions import GitlabCreateError, GitlabUpdateError

from pagure_exporter.conf import standard
from pagure_exporter.work.tkts import MoveTkts


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "data, rslt",
    [
        pytest.param(
            {
                "assignee": None,
                "blocks": [],
                "close_status": None,
                "closed_at": None,
                "closed_by": None,
                "comments": [],
                "content": "This is the body of the first test issue",
                "custom_fields": [],
                "date_created": "1697169462",
                "depends": [],
                "full_url": "https://pagure.io/protop2g-test-srce/issue/1",
                "id": 1,
                "last_updated": "1697169924",
                "milestone": None,
                "priority": None,
                "private": False,
                "related_prs": [],
                "status": "Open",
                "tags": ["aaaa", "bbbb"],
                "title": "This is the title of the first test issue",
                "user": {
                    "full_url": "https://fedoraproject.org",
                    "fullname": "Ordinary Engineer",
                    "name": "ordinaryengineer",
                    "url_path": "user/ordinaryengineer",
                },
            },
            False,
            id="Checking for possible errors while creating an issue ticket",  # noqa: E501
        )
    ]
)
def test_unit_gitlab_itertkts(caplog, data, rslt):
    test_movetkts = MoveTkts()

    # Store the previous state of the object so that it can be restored after mocking
    keepsake_gpro = standard.gpro

    # Mocking project object from the GitLab class and simulating a failure scenario
    standard.gpro = Mock()
    standard.gpro.issues.create.side_effect = GitlabCreateError()

    assert rslt == test_movetkts.itertkts(data)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gpro = keepsake_gpro


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "data, rslt",
    [
        pytest.param(
            {
                "comment": f"This test comment with broken links was created on {datetime.fromtimestamp(int(time()), timezone.utc).strftime('%c')}.",  # noqa: E501
                "date_created": str(int(time())),
                "edited_on": None,
                "editor": None,
                "id": 878473,
                "notification": False,
                "parent": None,
                "reactions": {},
                "user": {
                    "full_url": "https://fedoraproject.org",
                    "fullname": "Ordinary Engineer",
                    "name": "ordinaryengineer",
                    "url_path": "user/ordinaryengineer",
                },
            },
            False,
            id="Checking for possible errors while creating a comment under an existing issue ticket",  # noqa: E501
        ),
    ]
)
def test_unit_gitlab_itercmts(caplog, data, rslt):
    test_movetkts = MoveTkts()

    # Store the previous state of the object so that it can be restored after mocking
    keepsake_gpro = standard.gpro

    # Mocking project object from the GitLab class and simulating a failure scenario
    standard.gpro = Mock()
    standard.gpro.issues.get().discussions.create.side_effect = GitlabCreateError()

    assert rslt == test_movetkts.itercmts(data)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gpro = keepsake_gpro


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, root, tkid, shut, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            "https://gitlab.com/api/v4/projects",
            1,
            True,
            False,
            id="Checking for possible errors while updating the issue ticket status",  # noqa: E501
        ),
    ]
)
def test_unit_gitlab_iterstat(caplog, srce, dest, pkey, gkey, fusr, tusr, root, tkid, shut, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.gtlbtkid, standard.gtlblink, standard.isclosed = tkid, root, shut
    test_movetkts = MoveTkts()

    # Store the previous state of the object so that it can be restored after mocking
    keepsake_gpro = standard.gpro

    # Mocking project object from the GitLab class and simulating a failure scenario
    standard.gpro = Mock()
    standard.gpro.issues.get().save.side_effect = GitlabUpdateError()

    assert rslt == test_movetkts.iterstat()[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gpro = keepsake_gpro
