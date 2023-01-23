import requests


def rqsttick_pagu(paguname, pagucode, dataobjc):
    dicthead = {
        "Authorization": "token %s" % pagucode
    }
    tickloca = "https://pagure.io/api/0/%s/issues" % paguname
    optkjson = {
        "status": "Open",
        "page": "1",
        "per_page": "20",
    }
    optkrqst = requests.get(tickloca, params=optkjson, headers=dicthead)
    shtkjson = {
        "status": "Closed",
        "page": "1",
        "per_page": "20",
    }
    shtkrqst = requests.get(tickloca, params=shtkjson, headers=dicthead)
    if optkrqst.status_code == shtkrqst.status_code == 200:
        optkjson, shtkjson = optkrqst.json(), shtkrqst.json()
        dataobjc.pagurepo["estmtckt"] = {
            "open": int(optkjson["pagination"]["pages"]) * int(optkjson["pagination"]["per_page"]),
            "shut": int(shtkjson["pagination"]["pages"]) * int(shtkjson["pagination"]["per_page"]),
        }
    return optkrqst.status_code


def rqstproj_pagu(paguname, pagucode, dataobjc):
    dicthead = {
        "Authorization": "token %s" % pagucode
    }
    rqstloca = "https://pagure.io/api/0/%s" % paguname
    response = requests.get(rqstloca, headers=dicthead)
    if response.status_code == 200:
        jsondata = response.json()
        dataobjc.pagucode = pagucode
        dataobjc.paguname = paguname
        dataobjc.pagurepo = {
            "makedate": jsondata["date_created"],
            "lastmode": jsondata["date_modified"],
            "descript": jsondata["description"],
            "repolink": jsondata["full_url"],
            "reponame": jsondata["fullname"],
            "iden": jsondata["id"],
            "tags": jsondata["tags"],
            "main": {
                "username": jsondata["user"]["name"],
                "fullname": jsondata["user"]["fullname"],
            }
        }
    return response.status_code, response.reason


def rqstproj_gtlb(gtlbname, gtlbcode, dataobjc):
    dicthead = {
        "Authorization": "Bearer %s" % gtlbcode
    }
    rqstloca = "https://gitlab.com/api/v4/projects/%s" % gtlbname
    response = requests.get(rqstloca, headers=dicthead)
    if response.status_code == 200:
        jsondata = response.json()
        dataobjc.gtlbcode = gtlbcode
        dataobjc.gtlbname = gtlbname
        dataobjc.gtlbrepo = {
            "makedate": jsondata["created_at"],
            "lastmode": jsondata["last_activity_at"],
            "descript": jsondata["name_with_namespace"],
            "repolink": jsondata["web_url"],
            "reponame": jsondata["path_with_namespace"],
            "iden": jsondata["id"],
            "tags": jsondata["tag_list"],
            "main": {
                "username": jsondata["owner"]["username"],
                "fullname": jsondata["owner"]["name"]
            }
        }
    return response.status_code, response.reason


def rqstproj(paguname, pagucode, gtlbname, gtlbcode, dataobjc):
    pagurtrn = rqstproj_pagu(paguname, pagucode, dataobjc)
    gtlbrtrn = rqstproj_gtlb(gtlbname, gtlbcode, dataobjc)
    if pagurtrn[0] == 200:
        if gtlbrtrn[0] == 200:
            return True, 200, "done", "OK"
        else:
            return False, gtlbrtrn[0], "gtlb", gtlbrtrn[1]
    else:
        return False, pagurtrn[0], "pagu", pagurtrn[1]
