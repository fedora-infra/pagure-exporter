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


from datetime import datetime
from os import environ as envr
from time import time

import pytest

from pagure_exporter.conf import standard
from pagure_exporter.view.tkts import callwait
from pagure_exporter.work.tkts import MoveTkts


@pytest.mark.vcr(filter_headers=["Authorization"])
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


@pytest.mark.vcr(filter_headers=["Authorization"])
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


@pytest.mark.vcr(filter_headers=["Authorization"])
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


@pytest.mark.vcr(filter_headers=["Authorization"])
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


@pytest.mark.vcr(filter_headers=["Authorization"])
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


@pytest.mark.vcr(filter_headers=["Authorization"])
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


@pytest.mark.vcr(filter_headers=["Authorization"])
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
            "https://jitleb.com/api/v1212/projects",
            False,
            False,
            id="Attempting to migrate an existing issue ticket without tags to an invalid namespace",  # noqa: E501
        ),
    ],
)
def test_unit_itertkts(caplog, srce, dest, pkey, gkey, fusr, tusr, data, root, tags, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.gtlblink, standard.movetags = root, tags
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.itertkts(data)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gtlblink = "https://gitlab.com/api/v4/projects"


@pytest.mark.vcr(filter_headers=["Authorization"])
@pytest.mark.parametrize(
    "srce, dest, pkey, gkey, fusr, tusr, data, root, tkid, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            {
                "comment": f"This test comment with broken links was created on {datetime.utcfromtimestamp(int(time())).strftime('%c')}.",  # noqa: E501
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
            "https://gitlab.com/api/v4/projects",
            1,
            201,
            id="Attempting to migrate an existing comment to an existing namespace",
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
            id="Attempting to migrate an invalid comment to an existing namespace",
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            {
                "comment": f"This test comment with broken links was created on {datetime.utcfromtimestamp(int(time())).strftime('%c')}.",  # noqa: E501
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
            "https://jitleb.com/api/v1212/projects",
            1,
            False,
            id="Attempting to migrate an existing comment to an invalid namespace",
        ),
    ],
)
def test_unit_itercmts(caplog, srce, dest, pkey, gkey, fusr, tusr, data, root, tkid, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.gtlbtkid, standard.gtlblink = tkid, root
    test_movetkts = MoveTkts()
    assert rslt == test_movetkts.itercmts(data)[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gtlblink = "https://gitlab.com/api/v4/projects"


@pytest.mark.vcr(filter_headers=["Authorization"])
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
            200,
            id="Attempting to migrate status of an existing issue ticket when requested on an existing namespace",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            "https://gitlab.com/api/v4/projects",
            0,
            True,
            404,
            id="Attempting to migrate status of an invalid issue ticket when requested on an existing namespace",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            "https://jitleb.com/api/v1212/projects",
            1,
            True,
            False,
            id="Attempting to migrate status of an existing issue ticket when requested on an invalid namespace",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            envr["TEST_DEST"],
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            "https://gitlab.com/api/v4/projects",
            1,
            False,
            0,
            id="Attempting to migrate status of an existing issue ticket when not asked on an existing namespace",  # noqa: E501
        ),
    ],
)
def test_unit_iterstat(caplog, srce, dest, pkey, gkey, fusr, tusr, root, tkid, shut, rslt):
    standard.paguuser, standard.pagucode, standard.srcename = fusr, pkey, srce
    standard.gtlbuser, standard.gtlbcode, standard.destname = tusr, gkey, dest
    standard.gtlbtkid, standard.gtlblink, standard.isclosed = tkid, root, shut
    test_movetkts = MoveTkts()

    assert rslt == test_movetkts.iterstat()[0]  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.gtlblink = "https://gitlab.com/api/v4/projects"


@pytest.mark.parametrize(
    "rateindx, ratebond, waittime, text",
    [
        pytest.param(
            1,
            5,
            2,
            [],
            id="Testing to avoid waiting as the rate limit has not been reached",
        ),
        pytest.param(
            5,
            5,
            2,
            [
                "Rate limit reached - {ratebond} API requests made...",
                "Waiting for {waittime} second(s) and resetting the counter before resuming the transfer process",  # noqa: E501
            ],
            id="Testing to assert waiting as the rate limit has been reached",
        ),
    ],
)
def test_unit_callwait(caplog, rateindx, ratebond, waittime, text):
    standard.rateindx, standard.ratebond, standard.waittime = rateindx, ratebond, waittime

    strttime = time()
    callwait()
    stoptime = time()

    if rateindx < ratebond:
        assert (stoptime - strttime) <= standard.waittime  # noqa: S101
        assert standard.rateindx == 1  # noqa: S101

    if rateindx == ratebond:
        assert (stoptime - strttime) >= standard.waittime  # noqa: S101
        assert standard.rateindx == 0  # noqa: S101

    if rateindx == ratebond:
        text[0], text[1] = text[0].format(ratebond=ratebond), text[1].format(waittime=waittime)

    for indx in text:
        assert indx in caplog.text  # noqa: S101

    # Changing the shared variable back to its default
    # Please check https://github.com/gridhead/protop2g/issues/35 for additional details
    standard.rateindx, standard.ratebond, standard.waittime = 0, 500, 60
