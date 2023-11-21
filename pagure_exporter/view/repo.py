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


import sys

from pagure_exporter.conf import standard
from pagure_exporter.view.dcrt import failure, general, section, success, warning
from pagure_exporter.work.repo import PushRepo


def showrepo():
    try:
        section("Starting migration...")
        pushobjc = PushRepo()
        section("Attempting source namespace assets clone...")
        sclorslt = pushobjc.downsrce()
        if sclorslt[0]:
            success("Source namespace assets clone succeeded!")
            general("Directory: %s" % str(standard.srcecloc))
            general("Time taken: %s second(s)" % str(sclorslt[1]))
            section("Attempting destination namespace assets clone...")
            dclorslt = pushobjc.downdest()
            if dclorslt[0]:
                success("Destination namespace assets clone succeeded!")
                general("Directory: %s" % str(standard.destcloc))
                general("Time taken: %s second(s)" % str(dclorslt[1]))
                section("Reading branches data from the locally cloned assets...")
                sbrcrslt, dbrcrslt = pushobjc.cbrcsrce(), pushobjc.cbrcdest()
                if sbrcrslt[0] and dbrcrslt[0]:
                    success("Branches data reading succeeded!")
                    general("Available in source namespace: %d branch(es)" % len(standard.sbrcavbl))
                    for indx in standard.sbrcavbl:
                        general("  - (SRCE branch) %s" % str(indx))
                    general(
                        "Available in destination namespace: %d branch(es)" % len(standard.dbrcavbl)
                    )
                    for indx in standard.dbrcavbl:
                        general("  - (DEST branch) %s" % str(indx))
                    general("Requested for transferring: %d branch(es)" % len(standard.brtocopy))
                    for indx in standard.brtocopy:
                        general("  - (RQST branch) %s" % str(indx))
                    section("Initializing namespace assets transfer...")
                    tnfsrslt = pushobjc.tnfsrepo()
                    general(
                        "Assets transferred: %d branch(es) completed, %d branch(es) requested"
                        % (int(standard.tnfsindx), int(standard.tnfsqant))
                    )
                    general("Time taken: %s second(s)" % str(tnfsrslt[1]))
                    if tnfsrslt[0]:
                        if standard.tnfsindx == standard.tnfsqant:
                            success("Namespace assets transfer succeeded!")
                            sys.exit(0)
                        elif 0 < standard.tnfsindx < standard.tnfsqant:
                            warning("Namespace assets transfer partially completed!")
                            sys.exit(2)
                        else:  # pragma: no cover
                            # Tested already in `test_unit_tnfsrepo`
                            # From `test/test_unit_repo`
                            failure("Namespace assets transfer failed!")
                            sys.exit(1)
                    else:  # pragma: no cover
                        # Tested already in `test_unit_tnfsrepo`
                        # From `test/test_unit_repo`
                        failure("Namespace assets transfer failed!")
                        general("Exception occurred: %s" % str(tnfsrslt[1]))
                        sys.exit(1)
                else:  # pragma: no cover
                    # Tested already in `test_unit_cbrcsrce` and `test_unit_cbrcdest`
                    # From `test/test_unit_repo`
                    failure("Branches data reading failed!")
                    erormesg = str(sbrcrslt[1]) if not sbrcrslt[0] else str(dbrcrslt[1])
                    general("Exception occurred: %s" % erormesg)
                    sys.exit(1)
            else:  # pragma: no cover
                # Tested already in `test_unit_downdest`
                # From `test/test_unit_repo`
                failure("Destination namespace assets clone failed!")
                general("Exception occurred: %s" % str(dclorslt[1]))
                sys.exit(1)
        else:  # pragma: no cover
            # Tested already in `test_unit_downsrce`
            # From `test/test_unit_repo`
            failure("Source namespace assets clone failed!")
            general("Exception occurred: %s" % str(sclorslt[1]))
            sys.exit(1)
    except Exception as expt:
        failure("Migration failed!")
        general("Exception occurred: %s" % str(expt))
        sys.exit(1)
