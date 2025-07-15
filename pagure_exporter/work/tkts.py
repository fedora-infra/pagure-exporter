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


import time
from datetime import datetime, timezone

import requests
from gitlab import GitlabCreateError, GitlabGetError, GitlabUpdateError

from ..conf import standard


class MoveTickets:
    def __init__(self):
        self.pagure_url = f"{standard.pagure_api}/{standard.repo_srce}"
        self.gitlab_url = f"{standard.gitlab_api}/{standard.repo_dest}"
        self.pagure_header = {"Authorization": f"token {standard.pagure_token}"}
        self.gitlab_header = {"Authorization": f"Bearer {standard.gitlab_token}"}

    def get_ticket_count(self):
        try:
            start_time = time.time()
            initial_params = {"per_page": standard.page_size, "page": "1"}
            if standard.ticket_state == "closed" or standard.ticket_state == "all":
                initial_params["status"] = standard.ticket_state
            initial_response = requests.get(
                url=f"{self.pagure_url}/issues",
                params=initial_params,
                headers=self.pagure_header,
                timeout=standard.req_timeout,
            )
            status_code, reason = initial_response.status_code, initial_response.reason
            if status_code == 200:
                initial_response_data = initial_response.json()
                if initial_response_data["pagination"]["next"] is None:
                    standard.ticket_count = initial_response_data["total_issues"]
                else:
                    standard.page_index = int(initial_response_data["pagination"]["pages"])
                    final_params = {
                        "per_page": standard.page_size,
                        "page": standard.page_index,
                    }
                    if standard.ticket_state == "closed" or standard.ticket_state == "all":
                        final_params["status"] = standard.ticket_state
                    final_response = requests.get(
                        url=f"{self.pagure_url}/issues",
                        params=final_params,
                        headers=self.pagure_header,
                        timeout=standard.req_timeout,
                    )
                    status_code, reason = final_response.status_code, final_response.reason
                    if final_response.status_code == 200:
                        final_response_data = final_response.json()
                        total_issues = int(final_response_data["total_issues"])
                        standard.ticket_count = (
                            standard.page_index - 1
                        ) * standard.page_size + total_issues
            stop_time = time.time()
            elapsed_time = "%.2f" % (stop_time - start_time)
            return status_code, reason, elapsed_time
        except Exception as expt:
            return False, expt, "0"

    def iterate_page(self, page_number):
        try:
            start_time = time.time()
            params = {"per_page": standard.page_size, "page": f"{page_number}"}
            if standard.ticket_state == "closed" or standard.ticket_state == "all":
                params["status"] = standard.ticket_state
            response = requests.get(
                url=f"{self.pagure_url}/issues",
                params=params,
                headers=self.pagure_header,
                timeout=standard.req_timeout,
            )
            status_code, reason = response.status_code, response.reason
            if status_code == 200:
                standard.page_result = response.json()["issues"]
            stop_time = time.time()
            elapsed_time = "%.2f" % (stop_time - start_time)
            return status_code, reason, elapsed_time
        except Exception as expt:
            return False, expt, "0"

    def iterate_ticket_by_id(self, ticket_id):
        try:
            start_time = time.time()
            response = requests.get(
                url=f"{self.pagure_url}/issue/{ticket_id}",
                headers=self.pagure_header,
                timeout=standard.req_timeout,
            )
            status_code, skip_issue = response.status_code, True
            if status_code == 200:
                standard.ticket_result = response.json()
                # If the preferred ticket status is "FULL", all statuses must be addressed
                if (
                    standard.ticket_result["status"].lower() == standard.ticket_state == "closed"
                    or standard.ticket_result["status"].lower() == standard.ticket_state == "open"
                    or standard.ticket_state == "all"
                ):
                    skip_issue = False
            else:
                skip_issue = response.reason
            stop_time = time.time()
            elapsed_time = "%.2f" % (stop_time - start_time)
            return status_code, skip_issue, elapsed_time
        except Exception as expt:
            return False, expt, "0"

    def iterate_tickets(self, dict_object):
        try:
            start_time = time.time()
            standard.ticket_name = dict_object["title"]
            standard.ticket_identity = dict_object["id"]
            standard.ticket_closed = True if dict_object["status"] == "Closed" else False
            standard.author_name = dict_object["user"]["fullname"]
            standard.author_fas_url = f'{standard.fedora_acc}/{dict_object["user"]["url_path"]}'
            standard.author_id = dict_object["user"]["name"]
            standard.ticket_url = dict_object["full_url"]
            standard.ticket_labels = dict_object["tags"]
            standard.ticket_body = dict_object["content"]
            standard.ticket_secret = dict_object["private"]
            standard.issue_creation_time = int(dict_object["date_created"])
            header_data = standard.ticket_title_template.format(
                ticket_identity=standard.ticket_identity,
                ticket_name=standard.ticket_name,
            )
            body_data = standard.ticket_body_template.format(
                ticket_body=standard.ticket_body,
                ticket_url=standard.ticket_url,
                reponame=standard.repo_srce,
                repolink=standard.metadata_srce["repolink"],
                author_name=standard.author_name,
                author_fas_url=standard.author_fas_url,
                dateinfo=datetime.fromtimestamp(
                    standard.comment_creation_time, timezone.utc
                ).strftime("%c"),
                mo=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc)
                .strftime("%b")
                .lower(),
                dd=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%d"
                ),
                yy=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%Y"
                ),
                hh=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%H"
                ),
                mm=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%M"
                ),
            )
            """
            Replace "@" in the `header_data` and `body_data` with "&" to ensure that wrong people
            are not referenced in the destination namespace
            Check https://github.com/gridhead/pagure-exporter/issues/7 and
            https://github.com/fedora-infra/pagure-exporter/issues/204 for more information about
            the problem
            """
            request_data = {"title": header_data.replace("@", "&"), "description": body_data.replace("@", "&")}
            if standard.move_labels:
                request_data["labels"] = standard.ticket_labels
            if standard.move_secret:
                request_data["confidential"] = standard.ticket_secret
            if standard.move_sequence:
                request_data["iid"] = standard.ticket_identity
            result = standard.gitlab_project_obj.issues.create(data=request_data)
            status_code, reason = 201, result.web_url
            standard.gitlab_ticket_id = result.iid
            standard.issues_transferred += 1
            stop_time = time.time()
            elapsed_time = "%.2f" % (stop_time - start_time)
            return status_code, reason, elapsed_time
        except (GitlabCreateError, Exception) as expt:
            return False, expt, "0"

    def iterate_comments(self, dict_object):
        try:
            start_time = time.time()
            standard.comment_identity = dict_object["id"]
            standard.comment_url = f"{standard.ticket_url}#comment-{standard.comment_identity}"
            standard.comment_author = dict_object["user"]["fullname"]
            standard.comment_author_url = f'{standard.fedora_acc}/{dict_object["user"]["url_path"]}'
            standard.comment_creation_time = int(dict_object["date_created"])
            standard.comment_body = dict_object["comment"]
            body_data = standard.comment_body_template.format(
                comment_body=standard.comment_body,
                comment_url=standard.comment_url,
                comment_author=standard.comment_author,
                comment_author_url=standard.comment_author_url,
                ticket_url=standard.ticket_url,
                reponame=standard.repo_srce,
                repolink=standard.metadata_srce["repolink"],
                dateinfo=datetime.fromtimestamp(
                    standard.comment_creation_time, timezone.utc
                ).strftime("%c"),
                mo=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc)
                .strftime("%b")
                .lower(),
                dd=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%d"
                ),
                yy=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%Y"
                ),
                hh=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%H"
                ),
                mm=datetime.fromtimestamp(standard.comment_creation_time, timezone.utc).strftime(
                    "%M"
                ),
            )
            """
            Replace "@" in the `body_data` with "&" to ensure that wrong people are not referenced
            in the destination namespace
            Check https://github.com/gridhead/pagure-exporter/issues/7 for more information about
            the problem
            """
            request_data = {"body": body_data.replace("@", "&")}
            result = standard.gitlab_project_obj.issues.get(
                id=standard.gitlab_ticket_id
            ).discussions.create(data=request_data)
            status_code, reason = (
                201,
                f"{standard.metadata_dest['repolink']}/-/issues/{standard.gitlab_ticket_id}#note_{result.id}",  # noqa: E501
            )
            standard.comment_quantity += 1
            stop_time = time.time()
            elapsed_time = "%.2f" % (stop_time - start_time)
            return status_code, reason, elapsed_time
        except (GitlabCreateError, Exception) as expt:
            return False, expt, "0"

    def iterate_ticket_status(self):
        try:
            start_time, status_code, reason = time.time(), 0, ""
            if standard.ticket_closed:
                ticket = standard.gitlab_project_obj.issues.get(id=standard.gitlab_ticket_id)
                ticket.state_event = "close"
                ticket.save()
                status_code, reason = 200, "0"
            else:
                status_code, reason = 0, "0"
            stop_time = time.time()
            elapsed_time = "%.2f" % (stop_time - start_time)
            return status_code, reason, elapsed_time
        except (GitlabUpdateError, GitlabGetError, Exception) as expt:
            return False, str(expt), "0"
