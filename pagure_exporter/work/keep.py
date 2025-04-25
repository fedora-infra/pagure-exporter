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


from ..conf import standard


def storeinf(splt, dplt, srce, dest, pkey, gkey, fusr, tusr):
    standard.srcename = srce
    standard.destname = dest
    standard.pagucode = pkey
    standard.gtlbcode = gkey
    standard.paguuser = fusr
    standard.gtlbuser = tusr
    standard.pagulink = splt
    standard.gtlblink = dplt
    if not standard.pagulink.startswith("https://"):
        standard.pagulink = f"https://{standard.pagulink}"
    if not standard.pagulink.endswith("/api/0"):
        standard.pagulink = f"{standard.pagulink}/api/0"
    if not standard.gtlblink.startswith("https://"):
        standard.gtlblink = f"https://{standard.gtlblink}"
    if not standard.gtlblink.endswith("/api/v4/projects"):
        standard.gtlblink = f"{standard.gtlblink}/api/v4/projects"
    standard.frgesrce = standard.pagulink.replace("https://", "").replace("/api/0", "")
    standard.frgedest = standard.gtlblink.replace("https://", "").replace("/api/v4/projects", "")


def keepbrcs(brcs):
    standard.brtocopy = list(brcs)


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
