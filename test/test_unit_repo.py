import os
from os import environ as envr
from shutil import rmtree

import pytest

from protop2g.conf import standard  # noqa
from protop2g.work.repo import PushRepo

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
def test_unit_downsrce(caplog, srcename, destname, gkey, pkey, fusr, tusr, rslt):
    standard.paguuser, standard.pagucode = fusr, pkey
    standard.gtlbuser, standard.gtlbcode = tusr, gkey
    standard.srcehuto = (
        f"https://{standard.paguuser}:{standard.pagucode}@{standard.frgesrce}/{srcename}.git"
    )
    standard.desthuto = (
        f"https://{standard.gtlbuser}:{standard.gtlbcode}@{standard.frgedest}/{destname}.git"
    )
    assert rslt == PushRepo().downsrce()[0]  # noqa: S101


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
def test_unit_downdest(caplog, srcename, destname, gkey, pkey, fusr, tusr, rslt):
    standard.paguuser, standard.pagucode = fusr, pkey
    standard.gtlbuser, standard.gtlbcode = tusr, gkey
    standard.srcehuto = (
        f"https://{standard.paguuser}:{standard.pagucode}@{standard.frgesrce}/{srcename}.git"
    )
    standard.desthuto = (
        f"https://{standard.gtlbuser}:{standard.gtlbcode}@{standard.frgedest}/{destname}.git"
    )
    assert rslt == PushRepo().downdest()[0]  # noqa: S101


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, brcslist, pull, rslt",
    [
        pytest.param(
            envr["TEST_SRCE"],
            "gridhead/protop2g-test",
            envr["TEST_PKEY"],
            envr["TEST_GKEY"],
            envr["TEST_FUSR"],
            envr["TEST_TUSR"],
            ["test-aaaa", "test-bbbb", "test-cccc", "test-dddd"],
            False,
            True,
            id="Attempting to check the available branches for an source repository existing cloned copy",  # noqa: E501
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
            id="Attempting to check the available branches for an source repository invalid cloned copy",  # noqa: E501
        ),
    ],
)
def test_unit_cbrcsrce(caplog, srcename, destname, gkey, pkey, fusr, tusr, brcslist, pull, rslt):
    standard.paguuser, standard.pagucode = fusr, pkey
    standard.gtlbuser, standard.gtlbcode = tusr, gkey
    standard.srcehuto = (
        f"https://{standard.paguuser}:{standard.pagucode}@{standard.frgesrce}/{srcename}.git"
    )
    standard.desthuto = (
        f"https://{standard.gtlbuser}:{standard.gtlbcode}@{standard.frgedest}/{destname}.git"
    )
    test_pushrepo = PushRepo()
    test_pushrepo.downsrce()
    if pull:
        # This helps to simulate the condition where the temporary directories where the repository
        # assets were cloned locally was removed by an external factor
        rmtree(os.path.join(test_pushrepo.sloc.name, ".git"))
    assert rslt == test_pushrepo.cbrcsrce()[0]  # noqa: S101


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, pull, rslt",
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
            id="Attempting to check the available branches for an destination repository invalid cloned copy",  # noqa: E501
        ),
    ],
)
def test_unit_cbrcdest(caplog, srcename, destname, gkey, pkey, fusr, tusr, pull, rslt):
    standard.paguuser, standard.pagucode = fusr, pkey
    standard.gtlbuser, standard.gtlbcode = tusr, gkey
    standard.srcehuto = (
        f"https://{standard.paguuser}:{standard.pagucode}@{standard.frgesrce}/{srcename}.git"
    )
    standard.desthuto = (
        f"https://{standard.gtlbuser}:{standard.gtlbcode}@{standard.frgedest}/{destname}.git"
    )
    test_pushrepo = PushRepo()
    test_pushrepo.downdest()
    if pull:
        # This helps to simulate the condition where the temporary directories where the repository
        # assets were cloned locally was removed by an external factor
        rmtree(os.path.join(test_pushrepo.dloc.name, ".git"))
    assert rslt == test_pushrepo.cbrcdest()[0]  # noqa: S101


@pytest.mark.parametrize(
    "srcename, destname, pkey, gkey, fusr, tusr, brcs, pull, rslt",
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
            id="Attempting to migrate available branches from a source repository existing cloned copy with undefined branches",  # noqa: E501
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
            id="Attempting to migrate available branches from a source repository existing cloned copy while defining valid branches",  # noqa: E501
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
            id="Attempting to migrate available branches from a source repository existing cloned copy while defining invalid branches",  # noqa: E501
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
            id="Attempting to migrate available branches from a source repository invalid cloned copy with undefined branches",  # noqa: E501
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
            id="Attempting to migrate available branches from a source repository invalid cloned copy while defining valid branches",  # noqa: E501
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
            id="Attempting to migrate available branches from a source repository invalid cloned copy while defining invalid branches",  # noqa: E501
        ),
    ],
)
def test_unit_tnfsrepo(caplog, srcename, destname, gkey, pkey, fusr, tusr, brcs, pull, rslt):
    standard.paguuser, standard.pagucode = fusr, pkey
    standard.gtlbuser, standard.gtlbcode = tusr, gkey
    standard.srcehuto = (
        f"https://{standard.paguuser}:{standard.pagucode}@{standard.frgesrce}/{srcename}.git"
    )
    standard.desthuto = (
        f"https://{standard.gtlbuser}:{standard.gtlbcode}@{standard.frgedest}/{destname}.git"
    )
    standard.brtocopy = brcs
    test_pushrepo = PushRepo()
    test_pushrepo.downsrce()
    test_pushrepo.cbrcsrce()
    print(caplog)
    if pull:
        # This helps to simulate the condition where the temporary directories where the repository
        # assets were cloned locally was removed by an external factor
        rmtree(os.path.join(test_pushrepo.sloc.name, ".git"))
    assert rslt == test_pushrepo.tnfsrepo()[0]  # noqa: S101
