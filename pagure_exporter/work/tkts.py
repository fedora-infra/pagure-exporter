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


import time
from datetime import datetime, timezone

import requests
from gitlab import GitlabCreateError, GitlabGetError, GitlabUpdateError

from ..conf import standard


class MoveTkts:
    def __init__(self):
        self.purl = f"{standard.pagulink}/{standard.srcename}"
        self.gurl = f"{standard.gtlblink}/{standard.destname}"
        self.phed = {"Authorization": f"token {standard.pagucode}"}
        self.ghed = {"Authorization": f"Bearer {standard.gtlbcode}"}

    def getcount(self):
        try:
            strttime = time.time()
            initdata = {"per_page": standard.pagesize, "page": "1"}
            if standard.tktstate == "closed" or standard.tktstate == "all":
                initdata["status"] = standard.tktstate
            initresp = requests.get(
                url=f"{self.purl}/issues",
                params=initdata,
                headers=self.phed,
                timeout=standard.rqsttime,
            )
            respcode, respresn = initresp.status_code, initresp.reason
            if respcode == 200:
                initdict = initresp.json()
                if initdict["pagination"]["next"] is None:
                    standard.tktcount = initdict["total_issues"]
                else:
                    standard.pageqant = int(initdict["pagination"]["pages"])
                    lastdata = {
                        "per_page": standard.pagesize,
                        "page": standard.pageqant,
                    }
                    if standard.tktstate == "closed" or standard.tktstate == "all":
                        lastdata["status"] = standard.tktstate
                    lastresp = requests.get(
                        url=f"{self.purl}/issues",
                        params=lastdata,
                        headers=self.phed,
                        timeout=standard.rqsttime,
                    )
                    respcode, respresn = lastresp.status_code, lastresp.reason
                    if lastresp.status_code == 200:
                        lastdict = lastresp.json()
                        lastqant = int(lastdict["total_issues"])
                        standard.tktcount = (standard.pageqant - 1) * standard.pagesize + lastqant
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, respresn, timereqd
        except Exception as expt:
            return False, expt, "0"

    def iterpage(self, indx):
        try:
            strttime = time.time()
            rqstdata = {"per_page": standard.pagesize, "page": f"{indx}"}
            if standard.tktstate == "closed" or standard.tktstate == "all":
                rqstdata["status"] = standard.tktstate
            response = requests.get(
                url=f"{self.purl}/issues",
                params=rqstdata,
                headers=self.phed,
                timeout=standard.rqsttime,
            )
            respcode, respresn = response.status_code, response.reason
            if respcode == 200:
                standard.pagerslt = response.json()["issues"]
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, respresn, timereqd
        except Exception as expt:
            return False, expt, "0"

    def iteriden(self, tkid):
        try:
            strttime = time.time()
            response = requests.get(
                url=f"{self.purl}/issue/{tkid}",
                headers=self.phed,
                timeout=standard.rqsttime,
            )
            respcode, issuskip = response.status_code, True
            if respcode == 200:
                standard.issurslt = response.json()
                # If the preferred ticket status is "FULL", all statuses must be addressed
                if (
                    standard.issurslt["status"].lower() == standard.tktstate == "closed"
                    or standard.issurslt["status"].lower() == standard.tktstate == "open"
                    or standard.tktstate == "all"
                ):
                    issuskip = False
            else:
                issuskip = response.reason
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, issuskip, timereqd
        except Exception as expt:
            return False, expt, "0"

    def itertkts(self, dictobjc):
        try:
            strttime = time.time()
            standard.issuname = dictobjc["title"]
            standard.issuiden = dictobjc["id"]
            standard.isclosed = True if dictobjc["status"] == "Closed" else False
            standard.authname = dictobjc["user"]["fullname"]
            standard.authlink = f'{standard.fedora_acc}/{dictobjc["user"]["url_path"]}'
            standard.authorid = dictobjc["user"]["name"]
            standard.issulink = dictobjc["full_url"]
            standard.issutags = dictobjc["tags"]
            standard.issubody = dictobjc["content"]
            standard.issecret = dictobjc["private"]
            standard.timedata = int(dictobjc["date_created"])
            headdata = standard.headtemp_ticket.format(
                issuiden=standard.issuiden,
                issuname=standard.issuname,
                timeout=standard.rqsttime,
            )
            bodydata = standard.bodytemp_ticket.format(
                issubody=standard.issubody,
                issulink=standard.issulink,
                reponame=standard.srcename,
                repolink=standard.srcedict["repolink"],
                authname=standard.authname,
                authlink=standard.authlink,
                dateinfo=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%c"),
                mo=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%b").lower(),
                dd=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%d"),
                yy=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%Y"),
                hh=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%H"),
                mm=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%M"),
            )
            """
            Replace "@" in the `bodydata` with "&" to ensure that wrong people are not referenced
            in the destination namespace
            Check https://github.com/gridhead/pagure-exporter/issues/7 for more information about
            the problem
            """
            rqstdata = {"title": headdata, "description": bodydata.replace("@", "&")}
            if standard.movetags:
                rqstdata["labels"] = standard.issutags
            if standard.movehush:
                rqstdata["confidential"] = standard.issecret
            if standard.sequence:
                rqstdata["iid"] = standard.issuiden
            rslt = standard.gpro.issues.create(data=rqstdata)
            respcode, respresn = 201, rslt.web_url
            standard.gtlbtkid = rslt.iid
            standard.issutnfs += 1
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, respresn, timereqd
        except (GitlabCreateError, Exception) as expt:
            return False, expt, "0"

    def itercmts(self, dictobjc):
        try:
            strttime = time.time()
            standard.cmtsiden = dictobjc["id"]
            standard.cmtslink = f"{standard.issulink}#comment-{standard.cmtsiden}"
            standard.cmtsauth = dictobjc["user"]["fullname"]
            standard.cmtsaurl = f'{standard.fedora_acc}/{dictobjc["user"]["url_path"]}'
            standard.cmtstime = int(dictobjc["date_created"])
            standard.cmtsbody = dictobjc["comment"]
            bodydata = standard.bodytemp_cmts.format(
                cmtsbody=standard.cmtsbody,
                cmtslink=standard.cmtslink,
                cmtsauth=standard.cmtsauth,
                cmtsaurl=standard.cmtsaurl,
                issulink=standard.issulink,
                reponame=standard.srcename,
                repolink=standard.srcedict["repolink"],
                dateinfo=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%c"),
                mo=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%b").lower(),
                dd=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%d"),
                yy=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%Y"),
                hh=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%H"),
                mm=datetime.fromtimestamp(standard.cmtstime, timezone.utc).strftime("%M"),
            )
            """
            Replace "@" in the `bodydata` with "&" to ensure that wrong people are not referenced
            in the destination namespace
            Check https://github.com/gridhead/pagure-exporter/issues/7 for more information about
            the problem
            """
            rqstdata = {"body": bodydata.replace("@", "&")}
            rslt = standard.gpro.issues.get(id=standard.gtlbtkid).discussions.create(data=rqstdata)
            respcode, respresn = (
                201, f"{standard.destdict['repolink']}/-/issues/{standard.gtlbtkid}#note_{rslt.id}"
            )
            standard.cmtsqant += 1
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, respresn, timereqd
        except (GitlabCreateError, Exception) as expt:
            return False, expt, "0"

    def iterstat(self):
        try:
            strttime, respcode, respresn = time.time(), 0, ""
            if standard.isclosed:
                tkto = standard.gpro.issues.get(id=standard.gtlbtkid)
                tkto.state_event = "close"
                tkto.save()
                respcode, respresn = 200, "0"
            else:
                respcode, respresn = 0, "0"
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, respresn, timereqd
        except (GitlabUpdateError, GitlabGetError, Exception) as expt:
            return False, str(expt), "0"
