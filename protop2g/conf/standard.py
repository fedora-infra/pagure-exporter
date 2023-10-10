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

"""
STANDARD CONFIGURATION VARIABLES
"""

movecmts = False

movetags = False

tktgroup = []

movestat = False

tempdrct = "/var/tmp"
dfremote = "origin"
prfxsrce = "protop2g-tempsrce-"
prfxdest = "protop2g-tempdest-"
frgesrce = "pagure.io"
frgedest = "gitlab.com"
nrmtname = "freshsrc"

"""
INTERNAL CONFIGURATION VARIABLES
"""

paguuser = "UNAVAILABLE"
pagucode = "UNAVAILABLE"
srcename = "UNAVAILABLE"
pagulink = "https://pagure.io/api/0"
srcedict = {
    "makedate": "0",
    "lastmode": "0",
    "descript": "UNAVAILABLE",
    "repolink": "UNAVAILABLE",
    "reponame": "UNAVAILABLE",
    "identity": "UNAVAILABLE",
    "tagslist": [],
    "maintain": {
        "username": "UNAVAILABLE",
        "fullname": "UNAVAILABLE",
    },
}
srcehuto = "UNAVAILABLE"

gtlbuser = "UNAVAILABLE"
gtlbcode = "UNAVAILABLE"
destname = "UNAVAILABLE"
gtlblink = "https://gitlab.com/api/v4/projects"
destdict = {
    "makedate": "0",
    "lastmode": "0",
    "descript": "UNAVAILABLE",
    "repolink": "UNAVAILABLE",
    "reponame": "UNAVAILABLE",
    "identity": "UNAVAILABLE",
    "tagslist": [],
    "maintain": {
        "username": "UNAVAILABLE",
        "fullname": "UNAVAILABLE",
    },
}
desthuto = "UNAVAILABLE"

brtocopy = []
sbrcavbl = []
dbrcavbl = []
srcecloc = "UNAVAILABLE"
destcloc = "UNAVAILABLE"

# Current count of branches on the namespaces to be transferred
tnfsindx = 0

# Total quantity of branches on the namespaces to be transferred
tnfsqant = 0

# Number of issue ticket entities to be present on a response page of issues
pagesize = 35

# State of the issue ticket entities to be considered for transferring
tktstate = "open"

# Quantity of issue tickets available on the source namespace
tktcount = 0

# Current page number for probing into the available issue tickets in the source namespace
pageqant = 1

# List of issue ticket entities present on a response page of issues
pagerslt = []

# Dictionary of information pertaining to a single issue ticket made in the source namespace
issurslt = {}

# Title information of the issue ticket made in the source namespace
issuname = "UNAVAILABLE"

# Identity of the issue ticket made in the source namespace
issuiden = "0"

# Current status of the issue ticket made in the source namespace
isclosed = None

# Hyperlink of the issue ticket made in the source namespace
issulink = "UNAVAILABLE"

# Labels associated with the issue ticket made in the source namespace
issutags = []

# Textual information of the issue ticket made in the source namespace
issubody = "UNAVAILABLE"

# Username of the issue ticket made in the source namespace
authorid = "UNAVAILABLE"

# Full name of the issue ticket made in the source namespace
authname = "UNAVAILABLE"

# Fedora Account System URL for the author of the issue ticket made in the source namespace
authlink = "UNAVAILABLE"

# Creation datetime information of the issue ticket made in the source namespace
timedata = 0

# Identity of the issue ticket transferred to the destination namespace
gtlbtkid = "UNAVAILABLE"

# Quantity of issue tickets transferred to the destination namespace
issutnfs = 0

# Template for the title information of the issue tickets to be transferred
headtemp_ticket = "[SN#{issuiden}] {issuname}"

# Template for the textual information of the issue tickets to be transferred
bodytemp_ticket = """
{issubody}

_This issue ticket was originally created [here]({issulink}) on a Pagure repository, [**{reponame}**]({repolink})
by [**{authname}**]({authlink}) on [**{dateinfo}** UTC](https://savvytime.com/converter/utc/{mo}-{dd}-{yy}/{hh}-{mm})._

_This issue ticket was automatically created by the [**Pagure2GitLab Importer Service**]
(https://github.com/gridhead/protop2g)._
"""

# List of comment entities made under a ticket in the source namespace
issucmts = []

# Identity for the comments made under a ticket in the source namespace
cmtsiden = "UNAVAILABLE"

# Hyperlink for the comments made under a ticket in the source namespace
cmtslink = "UNAVAILABLE"

# Fullname of the author of the comments made under a ticket in the source namespace
cmtsauth = "UNAVAILABLE"

# Fedora Account System URL for the author of the comments made under a ticket in the source namespace
cmtsaurl = "UNAVAILABLE"

# Creation datetime information of the comments made under a ticket in the source namespace
cmtstime = 0

# Textual information of the comments made under a ticket in the source namespace
cmtsbody = "UNAVAILABLE"

# Hyperlink for the comments made under a transferred ticket in the destination namespace
gtlbcurl = "UNAVAILABLE"

# Quantity of comments made under a ticket in the source namespace
cmtsqant = 0

# Template for the textual information of the comments to be transferred
bodytemp_cmts = """
{cmtsbody}

_This comment was originally created [here]({cmtslink}) by [**{cmtsauth}**]({cmtsaurl})  under [this]({issulink}) issue
ticket on a Pagure repository, [**{reponame}**]({repolink}) on [**{dateinfo}** UTC]
(https://savvytime.com/converter/utc/{mo}-{dd}-{yy}/{hh}-{mm})._

_This comment was automatically created by the [**Pagure2GitLab Importer Service**]
(https://github.com/gridhead/protop2g)._
"""
