from protop2g.base import dfltpaguname, dfltrepodata


class Database(object):
    def __init__(self):
        self.paguname = dfltpaguname
        self.repodata = dfltrepodata


def revertdb(dataobjc):
    dataobjc.paguname = dfltpaguname
    dataobjc.reponame = dfltrepodata
