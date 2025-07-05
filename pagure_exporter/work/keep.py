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


def store_info(
    pagure_api,
    gitlab_api,
    repo_srce,
    repo_dest,
    pagure_token,
    gitlab_token,
    pagure_user,
    gitlab_user,
):
    standard.repo_srce = repo_srce
    standard.repo_dest = repo_dest
    standard.pagure_token = pagure_token
    standard.gitlab_token = gitlab_token
    standard.pagure_user = pagure_user
    standard.gitlab_user = gitlab_user
    standard.pagure_api = pagure_api
    standard.gitlab_api = gitlab_api
    if not standard.pagure_api.startswith("https://"):
        standard.pagure_api = f"https://{standard.pagure_api}"
    if not standard.pagure_api.endswith("/api/0"):
        standard.pagure_api = f"{standard.pagure_api}/api/0"
    if not standard.gitlab_api.startswith("https://"):
        standard.gitlab_api = f"https://{standard.gitlab_api}"
    if not standard.gitlab_api.endswith("/api/v4/projects"):
        standard.gitlab_api = f"{standard.gitlab_api}/api/v4/projects"
    standard.forge_srce = standard.pagure_api.replace("https://", "").replace("/api/0", "")
    standard.forge_dest = standard.gitlab_api.replace("https://", "").replace(
        "/api/v4/projects", ""
    )


def keep_branches(branches):
    standard.branches_to_copy = list(branches)


def keep_tags(tags):
    standard.tags_to_copy = list(tags)


def keep_tickets(status, ticket_group, comments, labels, state, secret, sequence):
    # Vote what kind of issue tickets are to be moved
    # Default Open
    if status == "SHUT":
        standard.ticket_state = "closed"
    elif status == "FULL":
        standard.ticket_state = "all"
    else:
        standard.ticket_state = "open"

    # Set a list of ticket identities to be moved
    # Default Empty
    standard.ticket_group = ticket_group

    # Vote if comments associated with the issue tickets are to be moved
    # Default False
    standard.move_comments = comments

    # Vote if labels associated with the issue tickets are to be moved
    # Default False
    standard.move_labels = labels

    # Vote if the state associated with the issue tickets are to be moved
    # Default False
    standard.move_state = state

    # Vote if the privacy associated with the issue tickets are to be moved
    # Default False
    standard.move_secret = secret

    # Vote if the identifier associated with the issue tickets are to be moved
    # Default False
    standard.move_sequence = sequence
