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


import os
from os import environ as envr
from shutil import rmtree

import pytest

from pagure_exporter.conf import standard
from pagure_exporter.work.repo import PushRepo

# TODO:
# Change the `gridhead/protop2g-test` static reference to a dynamic reference where the
# reponame is acquired using a helper function that outputs `reponame` when a project ID is
# fed for the destination namespace.


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            True,
            id="Attempting to clone an available source namespace",
        ),
        pytest.param(
            envr["TEST_SRCE"] + "ZEROEXISTENT",
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            False,
            id="Attempting to clone an invalid source namespace",
        ),
    ],
)
def test_unit_download_source(caplog, srcename, destname, gkey, pkey, fusr, tusr, rslt):
    standard.pagure_user, standard.pagure_token = fusr, pkey
    standard.gitlab_user, standard.gitlab_token = tusr, gkey
    standard.clone_url_srce = f"https://{standard.pagure_user}:{standard.pagure_token}@{standard.forge_srce}/{srcename}.git"
    standard.clone_url_dest = f"https://{standard.gitlab_user}:{standard.gitlab_token}@{standard.forge_dest}/{destname}.git"
    assert rslt == PushRepo().clone_source_repo()[0]  # noqa: S101


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            True,
            id="Attempting to clone an available destination namespace",
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test" + "ZEROEXISTENT",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            False,
            id="Attempting to clone an invalid destination namespace",
        ),
    ],
)
def test_unit_download_destination(caplog, srcename, destname, gkey, pkey, fusr, tusr, rslt):
    standard.pagure_user, standard.pagure_token = fusr, pkey
    standard.gitlab_user, standard.gitlab_token = tusr, gkey
    standard.clone_url_srce = f"https://{standard.pagure_user}:{standard.pagure_token}@{standard.forge_srce}/{srcename}.git"
    standard.clone_url_dest = f"https://{standard.gitlab_user}:{standard.gitlab_token}@{standard.forge_dest}/{destname}.git"
    assert rslt == PushRepo().clone_destination_repo()[0]  # noqa: S101


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, pull, rslt_branch, rslt_tag",
    [
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            False,
            True,
            True,
            id="Attempting to check the available branches and tags for an source repository existing cloned copy",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            True,
            False,
            False,
            id="Attempting to check the available branches and tags for an source repository invalid cloned copy",  # noqa: E501
        ),
    ],
)
def test_unit_check_source_assets(
    caplog, srcename, destname, gkey, pkey, fusr, tusr, pull, rslt_branch, rslt_tag
):
    standard.pagure_user, standard.pagure_token = fusr, pkey
    standard.gitlab_user, standard.gitlab_token = tusr, gkey
    standard.clone_url_srce = f"https://{standard.pagure_user}:{standard.pagure_token}@{standard.forge_srce}/{srcename}.git"
    standard.clone_url_dest = f"https://{standard.gitlab_user}:{standard.gitlab_token}@{standard.forge_dest}/{destname}.git"
    test_pushrepo = PushRepo()
    test_pushrepo.clone_source_repo()
    if pull:
        # This helps to simulate the condition where the temporary directories where the repository
        # assets were cloned locally was removed by an external factor
        rmtree(os.path.join(test_pushrepo.source_location.name, ".git"))
    assert rslt_branch == test_pushrepo.get_source_branches()[0]  # noqa: S101
    assert rslt_tag == test_pushrepo.get_source_tags()[0]  # noqa: S101


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, pull, rslt_branch, rslt_tag",
    [
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            False,
            True,
            True,
            id="Attempting to check the available branches for an destination repository existing cloned copy",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            True,
            False,
            False,
            id="Attempting to check the available branches for an destination repository invalid cloned copy",  # noqa: E501
        ),
    ],
)
def test_unit_check_destination_assets(
    caplog, srcename, destname, gkey, pkey, fusr, tusr, pull, rslt_branch, rslt_tag
):
    standard.pagure_user, standard.pagure_token = fusr, pkey
    standard.gitlab_user, standard.gitlab_token = tusr, gkey
    standard.clone_url_srce = f"https://{standard.pagure_user}:{standard.pagure_token}@{standard.forge_srce}/{srcename}.git"
    standard.clone_url_dest = f"https://{standard.gitlab_user}:{standard.gitlab_token}@{standard.forge_dest}/{destname}.git"
    test_pushrepo = PushRepo()
    test_pushrepo.clone_destination_repo()
    if pull:
        # This helps to simulate the condition where the temporary directories where the repository
        # assets were cloned locally was removed by an external factor
        rmtree(os.path.join(test_pushrepo.destination_location.name, ".git"))
    assert rslt_branch == test_pushrepo.get_destination_branches()[0]  # noqa: S101
    assert rslt_tag == test_pushrepo.get_destination_tags()[0]  # noqa: S101


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, brcs, pull, rslt_branch, rslt_tag",
    [
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            [],
            False,
            True,
            True,
            id="Attempting to migrate available branches and tags from a source repository existing cloned copy with undefined branches",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            ["test-aaaa", "test-bbbb"],
            False,
            True,
            True,
            id="Attempting to migrate available branches and tags from a source repository existing cloned copy while defining valid branches",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            ["test-axxa", "test-bxxb"],
            False,
            True,
            True,
            id="Attempting to migrate available branches and tags from a source repository existing cloned copy while defining invalid branches",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            [],
            True,
            False,
            False,
            id="Attempting to migrate available branches and tags from a source repository invalid cloned copy with undefined branches",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            ["test-aaaa", "test-bbbb"],
            True,
            False,
            False,
            id="Attempting to migrate available branches and tags from a source repository invalid cloned copy while defining valid branches",  # noqa: E501
        ),
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            ["test-axxa", "test-bxxb"],
            True,
            False,
            False,
            id="Attempting to migrate available branches and tags from a source repository invalid cloned copy while defining invalid branches",  # noqa: E501
        ),
    ],
)
def test_unit_tnfsrepo(
    caplog, srcename, destname, gkey, pkey, fusr, tusr, brcs, pull, rslt_branch, rslt_tag
):
    standard.pagure_user, standard.pagure_token = fusr, pkey
    standard.gitlab_user, standard.gitlab_token = tusr, gkey
    standard.clone_url_srce = f"https://{standard.pagure_user}:{standard.pagure_token}@{standard.forge_srce}/{srcename}.git"
    standard.clone_url_dest = f"https://{standard.gitlab_user}:{standard.gitlab_token}@{standard.forge_dest}/{destname}.git"
    standard.branches_to_copy = brcs
    test_pushrepo = PushRepo()
    test_pushrepo.clone_source_repo()
    test_pushrepo.get_source_branches()
    if pull:
        # This helps to simulate the condition where the temporary directories where the repository
        # assets were cloned locally was removed by an external factor
        rmtree(os.path.join(test_pushrepo.source_location.name, ".git"))
    assert rslt_branch == test_pushrepo.transfer_branches()[0]  # noqa: S101
    assert rslt_tag == test_pushrepo.transfer_tags()[0]  # noqa: S101
