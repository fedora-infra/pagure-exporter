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


import requests
from gitlab import Gitlab as gtlb
from gitlab import GitlabAuthenticationError, GitlabGetError

from ..conf import standard
from ..view.dcrt import conceal


class DataSrce:
    def __init__(self):
        self.repo = standard.repo_srce
        self.api = standard.pagure_api
        self.token = standard.pagure_token
        self.head = {"Authorization": "token %s" % self.token}

    def obtain_info(self):
        request_url = f"{self.api}/{self.repo}"
        response = requests.get(request_url, headers=self.head, timeout=standard.req_timeout)
        if response.status_code == 200:
            jsondict = response.json()
            standard.metadata_srce = {
                "makedate": jsondict["date_created"],
                "lastmode": jsondict["date_modified"],
                "descript": jsondict["description"],
                "repolink": jsondict["full_url"],
                "reponame": jsondict["fullname"],
                "identity": jsondict["id"],
                "tagslist": jsondict["tags"],
                "maintain": {
                    "username": jsondict["user"]["name"],
                    "fullname": jsondict["user"]["fullname"],
                },
            }
            standard.clone_url_srce = "https://{}:{}@{}/{}.git".format(
                standard.pagure_user,
                standard.pagure_token,
                standard.forge_srce,
                standard.metadata_srce["reponame"],
            )
            standard.display_url_srce = "https://{}:{}@{}/{}.git".format(
                standard.pagure_user,
                conceal(standard.pagure_token),
                standard.forge_srce,
                standard.metadata_srce["reponame"],
            )
        return response.status_code, response.reason


class DataDest:
    def __init__(self):
        self.repo = standard.repo_dest
        self.api = standard.gitlab_api
        self.token = standard.gitlab_token
        self.head = {"Authorization": "Bearer %s" % self.token}
        standard.gitlab_client_obj = gtlb(
            session=requests.Session(),
            url="https://gitlab.com",
            private_token=self.token,
            retry_transient_errors=True,
            timeout=standard.req_timeout,
        )

    def obtain_info(self):
        try:
            standard.gitlab_project_obj = standard.gitlab_client_obj.projects.get(
                id=standard.repo_dest
            )
            jsondict = standard.gitlab_project_obj.asdict()
            standard.metadata_dest = {
                "makedate": jsondict["created_at"],
                "lastmode": jsondict["last_activity_at"],
                "descript": jsondict["name_with_namespace"],
                "repolink": jsondict["web_url"],
                "reponame": jsondict["path_with_namespace"],
                "identity": jsondict["id"],
                "tagslist": jsondict["tag_list"],
                "maintain": {
                    "username": jsondict["namespace"]["path"],
                    "fullname": jsondict["namespace"]["name"],
                },
            }
            standard.clone_url_dest = jsondict["http_url_to_repo"]
            standard.clone_url_dest = "https://{}:{}@{}/{}.git".format(
                standard.gitlab_user,
                standard.gitlab_token,
                standard.forge_dest,
                standard.metadata_dest["reponame"],
            )
            standard.display_url_dest = "https://{}:{}@{}/{}.git".format(
                standard.gitlab_user,
                conceal(standard.gitlab_token),
                standard.forge_dest,
                standard.metadata_dest["reponame"],
            )
            return 200, "OK"
        except (GitlabAuthenticationError, GitlabGetError, Exception) as expt:
            return 0, str(expt)
