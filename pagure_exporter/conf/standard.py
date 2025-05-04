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


from logging import getLogger
from logging.config import dictConfig

"""
STANDARD CONFIGURATION VARIABLES
"""

move_comments = False

move_labels = False

move_state = False

move_secret = False

move_sequence = False

ticket_group = []

# While the location for creating temporary directories is definitive, the temporary directories
# are created with a random name constituting of a definitive prefix in runtime with only the user
# that created the file having READ and WRITE access to them. Basically, while the location
# `/var/tmp` is known from the beginning, the locations `/var/tmp/pexp-tempsrce-$RANDOM` and
# `/var/tmp/pexp-tempdest-$RANDOM` are not and hence - that should not be a security concern.
# For more information, please read
# https://bandit.readthedocs.io/en/latest/plugins/b108_hardcoded_tmp_directory.html
# https://security.openstack.org/guidelines/dg_using-temporary-files-securely.html
temp_dir = "/var/tmp"  # noqa: S108

# If a definitive timeout is not specified for every usage of `requests`, there is likeliness that
# a failure in probing a URL might lead to the program trying so indefinitely - thus causing the
# program to freeze. Remember, `requests` is a synchronous HTTP library and if you are looking for
# some of that nice asynchronicity, you are much better off using the likes of `httpx`.
# For more information, please read
# https://bandit.readthedocs.io/en/latest/plugins/b113_request_without_timeout.html
# https://datagy.io/python-requests-timeouts/
req_timeout = 60

default_remote = "origin"
temp_prefix_srce = "pexp-tempsrce-"
temp_prefix_dest = "pexp-tempdest-"
forge_srce = "pagure.io"
forge_dest = "gitlab.com"
new_remote = "freshsrc"
fedora_acc = "https://accounts.fedoraproject.org"
"""
INTERNAL CONFIGURATION VARIABLES
"""

pagure_user = "UNAVAILABLE"
pagure_token = "UNAVAILABLE"  # noqa: S105
repo_srce = "UNAVAILABLE"
pagure_api = "https://pagure.io/api/0"
metadata_srce = {
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
clone_url_srce = "UNAVAILABLE"
display_url_srce = "UNAVAILABLE"

gitlab_user = "UNAVAILABLE"
gitlab_token = "UNAVAILABLE"  # noqa: S105
repo_dest = "UNAVAILABLE"
gitlab_api = "https://gitlab.com/api/v4/projects"
metadata_dest = {
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
clone_url_dest = "UNAVAILABLE"
display_url_dest = "UNAVAILABLE"

branches_to_copy = []
available_branches_srce = []
available_branches_dest = []
clone_path_srce = "UNAVAILABLE"
clone_path_dest = "UNAVAILABLE"

# Regular expression to help detection of the GitLab Runners token in response body
detect = r"\b(?:glrt-|GR1348941)[\w\-]{20,23}"

# Placeholder string to substitute the detected GitLab Runners tokens in response body
cutout = "EXPUNGED"

# GitLab client object to be used while interacting with the destination namespace
gitlab_client_obj = None

# Project object of the destination namespace type of the GitLab client class
gitlab_project_obj = None

rate_index = 0

# Time in seconds to wait for when the rate limit for API requests is reached
wait_time = 60

# Current count of branches on the namespaces to be transferred
transfer_index = 0

# Total quantity of branches on the namespaces to be transferred
transfer_quantity = 0

# Number of issue ticket entities to be present on a response page of issues
page_size = 35

# State of the issue ticket entities to be considered for transferring
ticket_state = "open"

# Quantity of issue tickets available on the source namespace
ticket_count = 0

# Current page number for probing into the available issue tickets in the source namespace
page_index = 1

# List of issue ticket entities present on a response page of issues
page_result = []

# Dictionary of information pertaining to a single issue ticket made in the source namespace
ticket_result = {}

# Title information of the issue ticket made in the source namespace
ticket_name = "UNAVAILABLE"

# Identity of the issue ticket made in the source namespace
ticket_identity = "0"

# Current status of the issue ticket made in the source namespace
ticket_closed = None

# Hyperlink of the issue ticket made in the source namespace
ticket_url = "UNAVAILABLE"

# Labels associated with the issue ticket made in the source namespace
ticket_labels = []

# Textual information of the issue ticket made in the source namespace
ticket_body = "UNAVAILABLE"

# Privacy information of the issue ticket made in the source namespace
ticket_secret = "UNAVAILABLE"  # noqa: S105

# Username of the issue ticket made in the source namespace
author_id = "UNAVAILABLE"

# Full name of the issue ticket made in the source namespace
author_name = "UNAVAILABLE"

# Fedora Account System URL for the author of the issue ticket made in the source namespace
author_fas_url = "UNAVAILABLE"

# Creation datetime information of the issue ticket made in the source namespace
issue_creation_time = 0

# Identity of the issue ticket transferred to the destination namespace
gitlab_ticket_id = "UNAVAILABLE"

# Quantity of issue tickets transferred to the destination namespace
issues_transferred = 0

# Template for the title information of the issue tickets to be transferred
ticket_title_template = "[SN#{ticket_identity}] {ticket_name}"

# Template for the textual information of the issue tickets to be transferred
ticket_body_template = """
{ticket_body}

_This issue ticket was originally created [here]({ticket_url}) on a Pagure repository,
[**{reponame}**]({repolink}) by [**{author_name}**]({author_fas_url}) on
[**{dateinfo}** UTC](https://savvytime.com/converter/utc/{mo}-{dd}-{yy}/{hh}-{mm})._

_This issue ticket was automatically created by the
[**Pagure Exporter**](https://github.com/gridhead/pagure-exporter)._
"""

# List of comment entities made under a ticket in the source namespace
ticket_comments = []

# Identity for the comments made under a ticket in the source namespace
comment_identity = "UNAVAILABLE"

# Hyperlink for the comments made under a ticket in the source namespace
comment_url = "UNAVAILABLE"

# Fullname of the author of the comments made under a ticket in the source namespace
comment_author = "UNAVAILABLE"

# Fedora Account System URL for the author of the comments made under a ticket in the source
# namespace
comment_author_url = "UNAVAILABLE"

# Creation datetime information of the comments made under a ticket in the source namespace
comment_creation_time = 0

# Textual information of the comments made under a ticket in the source namespace
comment_body = "UNAVAILABLE"

# Hyperlink for the comments made under a transferred ticket in the destination namespace
gitlab_comment_url = "UNAVAILABLE"

# Quantity of comments made under a ticket in the source namespace
comment_quantity = 0

# Template for the textual information of the comments to be transferred
comment_body_template = """
{comment_body}

_This comment was originally created [here]({comment_url}) by [**{comment_author}**]({comment_author_url}) under
[this]({ticket_url}) issue ticket on a Pagure repository, [**{reponame}**]({repolink}) on
[**{dateinfo}** UTC](https://savvytime.com/converter/utc/{mo}-{dd}-{yy}/{hh}-{mm})._

_This comment was automatically created by the
[**Pagure Exporter**](https://github.com/gridhead/pagure-exporter)._
"""  # noqa: E501

# The default configuration for service logging
log_config = {
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

dictConfig(log_config)

logger = getLogger(__name__)
