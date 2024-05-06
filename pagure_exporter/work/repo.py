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


import os
import time
from tempfile import TemporaryDirectory

from git import Repo

from pagure_exporter.conf import standard
from pagure_exporter.view.misc import tnfsprog, tnfswarn


class PushRepo:
    def __init__(self):
        self.srce = standard.srcehuto
        self.dest = standard.desthuto
        self.pkey = standard.pagucode
        self.gkey = standard.gtlbcode
        self.brcs = standard.brtocopy
        self.sarg = dict(prefix=standard.prfxsrce, dir=standard.tempdrct)
        self.darg = dict(prefix=standard.prfxdest, dir=standard.tempdrct)
        self.sloc = TemporaryDirectory(**self.sarg)
        self.dloc = TemporaryDirectory(**self.darg)
        standard.srcecloc = self.sloc.name
        standard.destcloc = self.dloc.name

    def downsrce(self):
        try:
            strttime = time.time()
            Repo.clone_from(url=self.srce, to_path=self.sloc.name)
            stoptime = time.time()
            return True, "%.2f" % (stoptime - strttime)  # noqa : UP031
        except Exception as expt:
            return False, str(expt)

    def downdest(self):
        try:
            strttime = time.time()
            Repo.clone_from(url=self.dest, to_path=self.dloc.name)
            stoptime = time.time()
            return True, "%.2f" % (stoptime - strttime)  # noqa : UP031
        except Exception as expt:
            return False, str(expt)

    def cbrcsrce(self):
        if os.path.exists(os.path.join(self.sloc.name, ".git")):
            repoobjc = Repo(path=self.sloc.name)
            brcslist = [
                refx.name.replace(f"{standard.dfremote}/", "")
                for refx in repoobjc.remote(standard.dfremote).refs
            ]
            standard.sbrcavbl = list(brcslist)
            return True, brcslist
        else:
            return False, "Cloned source namespace assets could not be found"

    def cbrcdest(self):
        if os.path.exists(os.path.join(self.dloc.name, ".git")):
            repoobjc = Repo(path=self.dloc.name)
            brcslist = [
                refx.name.replace(f"{standard.dfremote}/", "")
                for refx in repoobjc.remote(standard.dfremote).refs
            ]
            standard.dbrcavbl = list(brcslist)
            return True, brcslist
        else:
            return False, "Cloned destination namespace assets could not be found"

    def tnfsrepo(self):
        if os.path.exists(os.path.join(self.sloc.name, ".git")):
            strttime = time.time()
            repoobjc = Repo(path=self.sloc.name)
            repoobjc.create_remote(standard.nrmtname, url=standard.desthuto)
            if len(standard.brtocopy) == 0:
                standard.tnfsqant = len(standard.sbrcavbl)
                tnfswarn(False, standard.tnfsqant)
                for brdx in standard.sbrcavbl:
                    repoobjc.git.checkout(f"{brdx}")
                    repoobjc.git.push(standard.nrmtname, "--set-upstream", brdx, "--force")
                    tnfsprog(
                        brdx,
                        standard.sbrcavbl.index(brdx) + 1,
                        len(standard.sbrcavbl),
                        True,
                    )
                    standard.tnfsindx += 1
            else:
                standard.tnfsqant = len(standard.brtocopy)
                tnfswarn(True, standard.tnfsqant)
                for brdx in standard.brtocopy:
                    if brdx in standard.sbrcavbl:
                        repoobjc.git.checkout(f"{brdx}")
                        repoobjc.git.push(standard.nrmtname, "--set-upstream", brdx, "--force")
                        tnfsprog(
                            brdx,
                            standard.brtocopy.index(brdx) + 1,
                            len(standard.brtocopy),
                            True,
                        )
                        standard.tnfsindx += 1
                    else:
                        tnfsprog(
                            brdx,
                            standard.brtocopy.index(brdx) + 1,
                            len(standard.brtocopy),
                            False,
                        )
            stoptime = time.time()
            return True, "%.2f" % (stoptime - strttime)  # noqa : UP031
        else:
            return False, "Cloned namespace assets could not be found"
