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

tnfsindx = 0
tnfsqant = 0

pagesize = 35
tktstate = "open"
tktcount = 0
pageqant = 1

pagerslt = []

issuname = "UNAVAILABLE"
issuiden = "0"
issulink = "UNAVAILABLE"
issubody = "UNAVAILABLE"
authorid = "UNAVAILABLE"
authname = "UNAVAILABLE"
authlink = "UNAVAILABLE"
timedata = 0
gtlbtkid = "UNAVAILABLE"

issutnfs = 0

headtemp_ticket = "[SN#{{ issuiden }}] {{ issuname }}"

bodytemp_ticket = """
{{ issubody }}

_This issue ticket was originally created [here]({{ issulink }}) on a Pagure repository, [**{{ reponame}}**]({{ repolink }}) by [**{{ authname }}**]({{ authlink }}) on [**{{ dateinfo }}** UTC](https://savvytime.com/converter/utc/{{ mo }}-{{ dd }}-{{ yy }}/{{ hh }}-{{ mm }})._

_This issue ticket was automatically created by the [**Pagure2GitLab Importer Service**](https://github.com/gridhead/protop2g)._
"""

issucmts = []

cmtsiden = "UNAVAILABLE"
cmtslink = "UNAVAILABLE"
cmtsauth = "UNAVAILABLE"
cmtsaurl = "UNAVAILABLE"
cmtstime = 0
cmtsbody = "UNAVAILABLE"
gtlbcurl = "UNAVAILABLE"

cmtsqant = 0

bodytemp_cmts = """
{{ cmtsbody }}

_This comment was originally created [here]({{ cmtslink }}) by [**{{ cmtsauth }}**]({{ cmtsaurl }})  under [this]({{ issulink }}) issue ticket on a Pagure repository, [**{{ reponame }}**]({{ repolink }}) on [**{{ dateinfo }}** UTC](https://savvytime.com/converter/utc/{{ mo }}-{{ dd }}-{{ yy }}/{{ hh }}-{{ mm }})._

_This comment was automatically created by the [**Pagure2GitLab Importer Service**](https://github.com/gridhead/protop2g)._
"""
