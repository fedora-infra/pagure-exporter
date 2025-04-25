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


class SrceData:
    def __init__(self):
        self.repo = standard.srcename
        self.loca = standard.pagulink
        self.code = standard.pagucode
        self.head = {"Authorization": "token %s" % self.code}

    def obtninfo(self):
        rqstloca = f"{self.loca}/{self.repo}"
        response = requests.get(rqstloca, headers=self.head, timeout=standard.rqsttime)
        if response.status_code == 200:
            jsondict = response.json()
            standard.srcedict = {
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
            standard.srcehuto = "https://{}:{}@{}/{}.git".format(
                standard.paguuser,
                standard.pagucode,
                standard.frgesrce,
                standard.srcedict["reponame"],
            )
            standard.srcedisp = "https://{}:{}@{}/{}.git".format(
                standard.paguuser,
                conceal(standard.pagucode),
                standard.frgesrce,
                standard.srcedict["reponame"],
            )
        return response.status_code, response.reason


class DestData:
    def __init__(self):
        self.repo = standard.destname
        self.loca = standard.gtlblink
        self.code = standard.gtlbcode
        self.head = {"Authorization": "Bearer %s" % self.code}
        standard.gobj = gtlb(
            session=requests.Session(),
            url="https://gitlab.com",
            private_token=self.code,
            retry_transient_errors=True,
            timeout=standard.rqsttime,
        )

    def obtninfo(self):
        try:
            standard.gpro = standard.gobj.projects.get(id=standard.destname)
            jsondict = standard.gpro.asdict()
            standard.destdict = {
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
            standard.desthuto = jsondict["http_url_to_repo"]
            standard.desthuto = "https://{}:{}@{}/{}.git".format(
                standard.gtlbuser,
                standard.gtlbcode,
                standard.frgedest,
                standard.destdict["reponame"],
            )
            standard.destdisp = "https://{}:{}@{}/{}.git".format(
                standard.gtlbuser,
                conceal(standard.gtlbcode),
                standard.frgedest,
                standard.destdict["reponame"],
            )
            return 200, "OK"
        except (GitlabAuthenticationError, GitlabGetError, Exception) as expt:
            return 0, str(expt)
