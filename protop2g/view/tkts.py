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


import sys

from protop2g.conf import standard
from protop2g.view.dcrt import failure, general, section, success, warning
from protop2g.work.tkts import MoveTkts


def showtkts():
    moveobjc = MoveTkts()
    section("Attempting source namespace issue ticket count...")
    warning(f"Migrating {'only ' if standard.tktstate == 'open' or standard.tktstate == 'closed' else ''}{standard.tktstate} issue tickets from the source namespace to the destination namespace")
    qantrslt = moveobjc.getcount()
    if qantrslt[0] == 200:
        success("Source namespace issue count succeeded!")
        general(f"Tickets matching criteria: {standard.tktcount} ticket(s)")
        general(f"Pages found: {standard.pageqant} page(s)")
        general(f"Time taken: {qantrslt[2]} second(s)")
        for indx in range(standard.pageqant):
            warning(f"Reading issue tickets information (Page {indx + 1} of {standard.pageqant})...")
            pagerslt = moveobjc.iterpage(indx + 1)
            if pagerslt[0] == 200:
                success("Issue ticket information reading succeeded!")
                general(f"Tickets on the page: {len(standard.pagerslt)} issue ticket(s)")
                general(f"Time taken: {qantrslt[2]} second(s)")
                for jndx in standard.pagerslt:
                    issurslt = moveobjc.itertkts(jndx)
                    section(f"Migrating issue ticket #{standard.issuiden} \"{standard.issuname}\" by \"{standard.authname} (ID {standard.authorid})\"...")
                    if issurslt[0] == 201:
                        success("Issue ticket migration succeeded!")
                        general(f"URL: {issurslt[1]}")
                        general(f"Time taken: {issurslt[2]} second(s)")
                    else:
                        success("Issue ticket migration failed!")
                        general("Code: %s" % str(issurslt[0]))
                        general("Reason: %s" % str(issurslt[1]))
                        general(f"Time taken: {issurslt[2]} second(s)")
                        exit(1)
            else:
                failure("Issue ticket information reading failed!")
                general("Code: %s" % str(pagerslt[0]))
                general("Reason: %s" % str(pagerslt[1]))
                general(f"Time taken: {pagerslt[2]} second(s)")
                exit(1)
        success("Namespace assets transferring queue processed!")
        general(f"{standard.issutnfs} issue ticket(s) transferred")
        sys.exit(0)
    else:
        failure("Source namespace issue count failed!")
        general("Code: %s" % str(qantrslt[0]))
        general("Reason: %s" % str(qantrslt[1]))
        general(f"Time taken: {qantrslt[2]} second(s)")
        exit(1)
