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


from datetime import datetime, timezone
from os import environ as envr
from time import time
from unittest.mock import Mock

import pytest
from gitlab.exceptions import GitlabCreateError, GitlabUpdateError

from pagure_exporter.conf import standard
from pagure_exporter.work.tkts import MoveTickets


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
    ],
)
def test_unit_gitlab_itertkts(caplog, data, rslt):
    test_movetkts = MoveTickets()

    # Store the previous state of the object so that it can be restored after mocking
    keepsake_gpro = standard.gitlab_project_obj

    # Mocking project object from the GitLab class and simulating a failure scenario
    standard.gitlab_project_obj = Mock()
    standard.gitlab_project_obj.issues.create.side_effect = GitlabCreateError()

    assert rslt == test_movetkts.iterate_tickets(data)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gitlab_project_obj = keepsake_gpro


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
    ],
)
def test_unit_gitlab_itercmts(caplog, data, rslt):
    test_movetkts = MoveTickets()

    # Store the previous state of the object so that it can be restored after mocking
    keepsake_gpro = standard.gitlab_project_obj

    # Mocking project object from the GitLab class and simulating a failure scenario
    standard.gitlab_project_obj = Mock()
    standard.gitlab_project_obj.issues.get().discussions.create.side_effect = GitlabCreateError()

    assert rslt == test_movetkts.iterate_comments(data)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gitlab_project_obj = keepsake_gpro


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
    ],
)
def test_unit_gitlab_iterstat(caplog, srce, dest, pkey, gkey, fusr, tusr, root, tkid, shut, rslt):
    standard.pagure_user, standard.pagure_token, standard.repo_srce = fusr, pkey, srce
    standard.gitlab_user, standard.gitlab_token, standard.repo_dest = tusr, gkey, dest
    standard.gitlab_ticket_id, standard.gitlab_api, standard.ticket_closed = tkid, root, shut
    test_movetkts = MoveTickets()

    # Store the previous state of the object so that it can be restored after mocking
    keepsake_gpro = standard.gitlab_project_obj

    # Mocking project object from the GitLab class and simulating a failure scenario
    standard.gitlab_project_obj = Mock()
    standard.gitlab_project_obj.issues.get().save.side_effect = GitlabUpdateError()

    assert rslt == test_movetkts.iterate_ticket_status()[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gitlab_project_obj = keepsake_gpro
