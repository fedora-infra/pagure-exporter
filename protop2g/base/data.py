from protop2g.base import dfltpaguname, dfltpagurepo, dfltpagucode, dfltgtlbname, dfltgtlbrepo, dfltgtlbcode


class Database(object):
    def __init__(self):
        self.paguname = dfltpaguname
        self.pagucode = dfltpagucode
        self.pagurepo = dfltpagurepo
        self.gtlbname = dfltgtlbname
        self.gtlbcode = dfltgtlbcode
        self.gtlbrepo = dfltgtlbrepo


def revertdb(dataobjc):
    dataobjc.paguname = dfltpaguname
    dataobjc.pagucode = dfltpagucode
    dataobjc.pagurepo = dfltpagurepo
    dataobjc.gtlbname = dfltgtlbname
    dataobjc.gtlbcode = dfltgtlbcode
    dataobjc.gtlbrepo = dfltgtlbrepo
