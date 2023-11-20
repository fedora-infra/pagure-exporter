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


from logging import getLogger
from logging.config import dictConfig

"""
STANDARD CONFIGURATION VARIABLES
"""

movecmts = False

movetags = False

tktgroup = []

movestat = False

# While the location for creating temporary directories is definitive, the temporary directories
# are created with a random name constituting of a definitive prefix in runtime with only the user
# that created the file having READ and WRITE access to them. Basically, while the location
# `/var/tmp` is known from the beginning, the locations `/var/tmp/pexp-tempsrce-$RANDOM` and
# `/var/tmp/pexp-tempdest-$RANDOM` are not and hence - that should not be a security concern.
# For more information, please read
# https://bandit.readthedocs.io/en/latest/plugins/b108_hardcoded_tmp_directory.html
# https://security.openstack.org/guidelines/dg_using-temporary-files-securely.html
tempdrct = "/var/tmp"  # noqa: S108

# If a definitive timeout is not specified for every usage of `requests`, there is likeliness that
# a failure in probing a URL might lead to the program trying so indefinitely - thus causing the
# program to freeze. Remember, `requests` is a synchronous HTTP library and if you are looking for
# some of that nice asynchronicity, you are much better off using the likes of `httpx`.
# For more information, please read
# https://bandit.readthedocs.io/en/latest/plugins/b113_request_without_timeout.html
# https://datagy.io/python-requests-timeouts/
rqsttime = 60

dfremote = "origin"
prfxsrce = "pexp-tempsrce-"
prfxdest = "pexp-tempdest-"
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
srcedisp = "UNAVAILABLE"

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
destdisp = "UNAVAILABLE"

brtocopy = []
sbrcavbl = []
dbrcavbl = []
srcecloc = "UNAVAILABLE"
destcloc = "UNAVAILABLE"

rateindx = 0

# Time in seconds to wait for when the rate limit for API requests is reached
waittime = 60

# Rate limit for API requests as defined by the destination forge
ratebond = 500

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

_This issue ticket was originally created [here]({issulink}) on a Pagure repository,
[**{reponame}**]({repolink}) by [**{authname}**]({authlink}) on
[**{dateinfo}** UTC](https://savvytime.com/converter/utc/{mo}-{dd}-{yy}/{hh}-{mm})._

_This issue ticket was automatically created by the
[**Pagure Exporter**](https://github.com/gridhead/pagure-exporter)._
"""

# List of comment entities made under a ticket in the source namespace
issucmts = []

# Identity for the comments made under a ticket in the source namespace
cmtsiden = "UNAVAILABLE"

# Hyperlink for the comments made under a ticket in the source namespace
cmtslink = "UNAVAILABLE"

# Fullname of the author of the comments made under a ticket in the source namespace
cmtsauth = "UNAVAILABLE"

# Fedora Account System URL for the author of the comments made under a ticket in the source
# namespace
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

_This comment was originally created [here]({cmtslink}) by [**{cmtsauth}**]({cmtsaurl}) under
[this]({issulink}) issue ticket on a Pagure repository, [**{reponame}**]({repolink}) on
[**{dateinfo}** UTC](https://savvytime.com/converter/utc/{mo}-{dd}-{yy}/{hh}-{mm})._

_This comment was automatically created by the
[**Pagure Exporter**](https://github.com/gridhead/pagure-exporter)._
"""

# The default configuration for service logging
logrconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}

dictConfig(logrconf)

logger = getLogger(__name__)
