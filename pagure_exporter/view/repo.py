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
            general(f"Directory: {standard.srcecloc}")
            general(f"Time taken: {sclorslt[1]} second(s)")
            section("Attempting destination namespace assets clone...")
            dclorslt = pushobjc.downdest()
            if dclorslt[0]:
                success("Destination namespace assets clone succeeded!")
                general(f"Directory: {standard.destcloc}")
                general(f"Time taken: {dclorslt[1]} second(s)")
                section("Reading branches data from the locally cloned assets...")
                sbrcrslt, dbrcrslt = pushobjc.cbrcsrce(), pushobjc.cbrcdest()
                if sbrcrslt[0] and dbrcrslt[0]:
                    success("Branches data reading succeeded!")
                    general(f"Available in source namespace: {len(standard.sbrcavbl)} branch(es)")
                    for indx in standard.sbrcavbl:
                        general(f"  - (SRCE branch) {indx}")
                    general(
                        f"Available in destination namespace: {len(standard.dbrcavbl)} branch(es)"
                    )
                    for indx in standard.dbrcavbl:
                        general(f"  - (DEST branch) {indx}")
                    general(f"Requested for transferring: {standard.brtocopy} branch(es)")
                    for indx in standard.brtocopy:
                        general(f"  - (RQST branch) {indx}")
                    section("Initializing namespace assets transfer...")
                    tnfsrslt = pushobjc.tnfsrepo()
                    general(
                        f"Assets transferred: {standard.tnfsindx} branch(es) completed, {standard.tnfsqant} branch(es) requested"  # noqa : E501
                    )
                    general(f"Time taken: {tnfsrslt[1]} second(s)")
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
                        general(f"Exception occurred: {tnfsrslt[1]}")
                        sys.exit(1)
                else:  # pragma: no cover
                    # Tested already in `test_unit_cbrcsrce` and `test_unit_cbrcdest`
                    # From `test/test_unit_repo`
                    failure("Branches data reading failed!")
                    erormesg = str(sbrcrslt[1]) if not sbrcrslt[0] else str(dbrcrslt[1])
                    general(f"Exception occurred: {erormesg}")
                    sys.exit(1)
            else:  # pragma: no cover
                # Tested already in `test_unit_downdest`
                # From `test/test_unit_repo`
                failure("Destination namespace assets clone failed!")
                general(f"Exception occurred: {dclorslt[1]}")
                sys.exit(1)
        else:  # pragma: no cover
            # Tested already in `test_unit_downsrce`
            # From `test/test_unit_repo`
            failure("Source namespace assets clone failed!")
            general(f"Exception occurred: {sclorslt[1]}")
            sys.exit(1)
    except Exception as expt:
        failure("Migration failed!")
        general(f"Exception occurred: {expt}")
        sys.exit(1)
