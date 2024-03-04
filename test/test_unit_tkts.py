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
from gitlab import Gitlab as gtlb
from requests import Session

from pagure_exporter.conf import standard
from pagure_exporter.work.tkts import MoveTkts


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, qant, stat, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            2,
            "all",
            200,
            id="Attempting to count issue tickets from a valid issue tracker of smaller length",
        ),
        pytest.param(
            "fedora-infrastructure",
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            10000,
            "all",
            200,
            id="Attempting to count issue tickets from a valid issue tracker of longer length",
        ),
    ],
)
def test_unit_getcount(caplog, srce, dest, pkey, gkey, fusr, tusr, qant, stat, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.tktstate = stat
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.getcount()[0]  # noqa: S101
    assert qant <= standard.tktcount  # noqa: S101


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, root, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            "https://pagure.io/api/0",
            200,
            id="Attempting to count issue tickets from an existing issue tracker on an existing forge",  # noqa: E501
        ),
        pytest.param(
            "stoopeed-repo",
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            "https://pagure.io/api/0",
            404,
            id="Attempting to count issue tickets from an invalid issue tracker on an existing forge",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            "https://pajure.io/api/0",
            False,
            id="Attempting to count issue tickets from an existing issue tracker on an invalid forge",  # noqa: E501
        ),
    ],
)
def test_unit_getcount_expt(caplog, srce, dest, pkey, gkey, fusr, tusr, root, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.pagulink = root
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.getcount()[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.pagulink = "https://pagure.io/api/0"


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, size, indx, stat, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            0,
            1,
            "",
            400,
            id="Setting an invalid `pagesize` value",
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            1,
            "",
            200,
            id="Attempting to iterate through the first page from an existing issue tracker for OPEN tickets",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            1,
            "closed",
            200,
            id="Attempting to iterate through the first page from an existing issue tracker for SHUT tickets",  # noqa: E501
        ),
    ],
)
def test_unit_iterpage(caplog, srce, dest, pkey, gkey, fusr, tusr, size, indx, stat, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.pagesize, standard.tktstate = size, stat
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.iterpage(indx)[0]  # noqa: S101


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, indx, root, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            "https://pagure.io/api/0",
            200,
            id="Attempting to iterate through the first page from an existing issue tracker on an existing forge",  # noqa: E501
        ),
        pytest.param(
            "stoopeed-repo",
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            "https://pagure.io/api/0",
            404,
            id="Attempting to iterate through the first page from an invalid issue tracker on an existing forge",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            "https://pajure.io/api/0",
            False,
            id="Attempting to iterate through the first page from an existing issue tracker on an invalid forge",  # noqa: E501
        ),
    ],
)
def test_unit_iterpage_expt(caplog, srce, dest, pkey, gkey, fusr, tusr, indx, root, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.pagulink = root
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.iterpage(indx)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.pagulink = "https://pagure.io/api/0"


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, indx, stat, skip, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            "open",
            False,
            200,
            id="Attempting to probe the issue ticket with the existing identity with matching status",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            2,
            "open",
            True,
            200,
            id="Attempting to probe the issue ticket with the existing identity with mismatch status",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1212,
            "shut",
            False,
            404,
            id="Attempting to probe the issue ticket with the invalid identity",
        ),
    ],
)
def test_unit_iteriden(caplog, srce, dest, pkey, gkey, fusr, tusr, indx, stat, skip, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.tktstate = stat
    test_movetkts = MoveTkts()
    test_iteriden = test_movetkts.iteriden(indx)
    assert rslt == test_iteriden[0]  # noqa: S101
    if rslt == 200:
        assert skip == test_iteriden[1]  # noqa: S101


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, indx, root, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            "https://pagure.io/api/0",
            200,
            id="Attempting to probe the issue ticket with the existing identity on an existing issue tracker on an existing forge",  # noqa: E501
        ),
        pytest.param(
            "stoopeed-repo",
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            "https://pagure.io/api/0",
            404,
            id="Attempting to iterate through the first page from an invalid issue tracker on an existing forge",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            1,
            "https://pajure.io/api/0",
            False,
            id="Attempting to iterate through the first page from an existing issue tracker on an invalid forge",  # noqa: E501
        ),
    ],
)
def test_unit_iteriden_expt(caplog, srce, dest, pkey, gkey, fusr, tusr, indx, root, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.pagulink = root
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.iteriden(indx)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.pagulink = "https://pagure.io/api/0"


@pytest.mark.vcr(filter_headers=["Authorization", "PRIVATE-TOKEN"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, data, root, tags, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
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
            "https://gitlab.com/api/v4/projects",
            False,
            201,
            id="Attempting to migrate an existing issue ticket without tags to an existing namespace",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
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
            "https://gitlab.com/api/v4/projects",
            True,
            201,
            id="Attempting to migrate an existing issue ticket with tags to an existing namespace",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            {
                "Is this a valid format?": False,
            },
            "https://gitlab.com/api/v4/projects",
            False,
            False,
            id="Attempting to migrate an invalid issue ticket without tags to an existing namespace",  # noqa: E501
        ),
    ],
)
def test_unit_itertkts(caplog, srce, dest, pkey, gkey, fusr, tusr, data, root, tags, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.gtlblink, standard.movetags = root, tags

    keepsake_gpro = standard.gpro
    standard.gpro = gtlb(
            session=Session(),
            url="https://gitlab.com",
            private_token=standard.gtlbcode,
            retry_transient_errors=True,
            timeout=standard.rqsttime,
        ).projects.get(id=standard.destname)
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.itertkts(data)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gtlblink = "https://gitlab.com/api/v4/projects"
    standard.gpro = keepsake_gpro
