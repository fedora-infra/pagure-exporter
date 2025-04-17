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

import sys
from pagure_exporter.conf import standard
from pagure_exporter.view.dcrt import failure


def storeinf(platform, srce, dest, pkey, gkey, fusr, tusr):
    standard.srcename = srce
    standard.destname = dest
    standard.srcecode = pkey
    standard.gtlbcode = gkey
    standard.srceuser = fusr
    standard.gtlbuser = tusr
    standard.srcelink, standard.frgesrce = keepplatform(platform)


def keepbrcs(brcs):
    standard.brtocopy = list(brcs)


def keepplatform(platform):
    if platform == "pagure":
        return standard.pagulink, "pagure.io"
    elif platform == "centos":
        return standard.centoslink, "git.centos.org"
    else:
        failure("Invalid Source Git platform name")
        sys.exit(1)


def keeptkts(status, tktgroup, comments, labels, commit, secret, series):
    # Vote what kind of issue tickets are to be moved
    # Default Open
    if status == "SHUT":
        standard.tktstate = "closed"
    elif status == "FULL":
        standard.tktstate = "all"
    else:
        standard.tktstate = "open"

    # Set a list of ticket identities to be moved
    # Default Empty
    standard.tktgroup = tktgroup

    # Vote if comments associated with the issue tickets are to be moved
    # Default False
    standard.movecmts = comments

    # Vote if labels associated with the issue tickets are to be moved
    # Default False
    standard.movetags = labels

    # Vote if the state associated with the issue tickets are to be moved
    # Default False
    standard.movestat = commit

    # Vote if the privacy associated with the issue tickets are to be moved
    # Default False
    standard.movehush = secret

    # Vote if the identifier associated with the issue tickets are to be moved
    # Default False
    standard.sequence = series
