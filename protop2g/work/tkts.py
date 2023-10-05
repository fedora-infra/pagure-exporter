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


import time
from datetime import datetime

import requests

from protop2g.conf import standard


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
            initresp = requests.get(url=f"{self.purl}/issues", params=initdata, headers=self.phed)
            respcode, respresn = initresp.status_code, initresp.reason
            if respcode == 200:
                initdict = initresp.json()
                if initdict["pagination"]["next"] == None:
                    standard.tktcount = initdict["total_issues"]
                else:
                    standard.pageqant = int(initdict["pagination"]["pages"])
                    lastdata = {"per_page": standard.pagesize, "page": standard.pageqant}
                    if standard.tktstate == "closed" or standard.tktstate == "all":
                        lastdata["status"] = standard.tktstate
                    lastresp = requests.get(
                        url=f"{self.purl}/issues", params=lastdata, headers=self.phed
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
            response = requests.get(url=f"{self.purl}/issues", params=rqstdata, headers=self.phed)
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
            response = requests.get(url=f"{self.purl}/issue/{tkid}", headers=self.phed)
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
            standard.authname = dictobjc["user"]["fullname"]
            standard.authlink = dictobjc["user"]["full_url"]
            standard.authorid = dictobjc["user"]["name"]
            standard.issulink = dictobjc["full_url"]
            standard.issutags = dictobjc["tags"]
            standard.issubody = dictobjc["content"]
            standard.timedata = int(dictobjc["date_created"])
            headdata = standard.headtemp_ticket.format(
                issuiden=standard.issuiden, issuname=standard.issuname
            )
            bodydata = standard.bodytemp_ticket.format(
                issubody=standard.issubody,
                issulink=standard.issulink,
                reponame=standard.srcename,
                repolink=standard.srcedict["repolink"],
                authname=standard.authname,
                authlink=standard.authlink,
                dateinfo=datetime.utcfromtimestamp(standard.timedata).strftime("%c"),
                mo=datetime.utcfromtimestamp(standard.timedata).strftime("%b").lower(),
                dd=datetime.utcfromtimestamp(standard.timedata).strftime("%d"),
                yy=datetime.utcfromtimestamp(standard.timedata).strftime("%Y"),
                hh=datetime.utcfromtimestamp(standard.timedata).strftime("%H"),
                mm=datetime.utcfromtimestamp(standard.timedata).strftime("%M"),
            )
            """
            Replace "@" in the `bodydata` with "&" to ensure that wrong people are not referenced in the destination namespace
            Check https://github.com/gridhead/protop2g/issues/7 for more information about the problem
            """
            rqstdata = {"title": headdata, "description": bodydata.replace("@", "&")}
            if standard.movetags:
                rqstdata["labels"] = ",".join(standard.issutags)
            response = requests.post(url=f"{self.gurl}/issues", data=rqstdata, headers=self.ghed)
            respcode, respresn = response.status_code, response.reason
            if respcode == 201:
                respresn = response.json()["web_url"]
                standard.gtlbtkid = response.json()["iid"]
                standard.issutnfs += 1
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, respresn, timereqd
        except Exception as expt:
            return False, expt, "0"

    def itercmts(self, dictobjc):
        try:
            strttime = time.time()
            standard.cmtsiden = dictobjc["id"]
            standard.cmtslink = f"{standard.issulink}#comment-{standard.cmtsiden}"
            standard.cmtsauth = dictobjc["user"]["fullname"]
            standard.cmtsaurl = dictobjc["user"]["full_url"]
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
                dateinfo=datetime.utcfromtimestamp(standard.cmtstime).strftime("%c"),
                mo=datetime.utcfromtimestamp(standard.cmtstime).strftime("%b").lower(),
                dd=datetime.utcfromtimestamp(standard.cmtstime).strftime("%d"),
                yy=datetime.utcfromtimestamp(standard.cmtstime).strftime("%Y"),
                hh=datetime.utcfromtimestamp(standard.cmtstime).strftime("%H"),
                mm=datetime.utcfromtimestamp(standard.cmtstime).strftime("%M"),
            )
            """
            Replace "@" in the `bodydata` with "&" to ensure that wrong people are not referenced in the destination namespace
            Check https://github.com/gridhead/protop2g/issues/7 for more information about the problem
            """
            rqstdata = {"body": bodydata.replace("@", "&")}
            response = requests.post(
                url=f"{self.gurl}/issues/{standard.gtlbtkid}/notes",
                data=rqstdata,
                headers=self.ghed,
            )
            respcode, respresn = response.status_code, response.reason
            if respcode == 201:
                respresn = f"{standard.destdict['repolink']}/-/issues/{standard.gtlbtkid}#note_{response.json()['id']}"
                standard.cmtsqant += 1
            stoptime = time.time()
            timereqd = "%.2f" % (stoptime - strttime)
            return respcode, respresn, timereqd
        except Exception as expt:
            return False, expt, "0"
