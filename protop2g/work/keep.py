"""
protop2g
Copyright (C) 2022-2023 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source
code or documentation are not subject to the GNU General Public
License and may only be used or replicated with the express permission
of Red Hat, Inc.
"""


from protop2g.conf import standard


def storeinf(srce, dest, pkey, gkey, fusr, tusr):
    standard.srcename = srce
    standard.destname = dest
    standard.pagucode = pkey
    standard.gtlbcode = gkey
    standard.paguuser = fusr
    standard.gtlbuser = tusr


def keepbrcs(brcs):
    standard.brtocopy = list(brcs)


def keepqant(qant):
    if qant == "shut":
        standard.tktstate = "closed"
    elif qant == "full":
        standard.tktstate = "all"
    else:
        standard.tktstate = "open"


def keepcmts(comments):
    standard.movecmts = comments


def keeptkts(qant, comments, labels):
    # Vote what kind of issue tickets are to be moved
    # Default Open
    if qant == "shut":
        standard.tktstate = "closed"
    elif qant == "full":
        standard.tktstate = "all"
    else:
        standard.tktstate = "open"

    # Vote if comments associated with the issue tickets are to be moved
    # Default False
    standard.movecmts = comments

    # Vote if labels associated with the issue tickets are to be moved
    # Default False
    standard.movetags = labels
