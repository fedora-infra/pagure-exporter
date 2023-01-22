import requests


def rqstrepo(paguname, dataobjc):
    rqstloca = "https://pagure.io/api/0/%s" % paguname
    response = requests.get(rqstloca)
    if response.status_code == 200:
        jsondata = response.json()
        dataobjc.paguname = paguname
        dataobjc.repodata = {
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
        return True, response.status_code
    else:
        return False, response.status_code
