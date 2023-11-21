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
import time

from pagure_exporter.conf import standard
from pagure_exporter.view.dcrt import failure, general, section, success, warning
from pagure_exporter.work.tkts import MoveTkts


def callwait():
    if standard.rateindx == standard.ratebond:
        warning(f"Rate limit reached - {standard.ratebond} API requests made...")
        general(
            f"Waiting for {standard.waittime} second(s) and resetting the counter before resuming the transfer process"  # noqa: E501
        )
        time.sleep(standard.waittime)
        standard.rateindx = 0


def showtkts():
    moveobjc = MoveTkts()
    section("Attempting source namespace issue ticket count...")
    warning(
        f"Extracting {'all ' if standard.tktstate == 'open' or standard.tktstate == 'closed' else ''}"  # noqa: E501
        f"{standard.tktstate} issue tickets {'with' if standard.movetags else 'without'} labels, "
        f"{'with' if standard.movestat else 'without'} states, "
        f"{'with' if standard.movehush else 'without'} privacy and "
        f"{'with' if standard.movecmts else 'without'} comments off the given selection"
    )
    if not standard.tktgroup:
        qantrslt = moveobjc.getcount()
        if qantrslt[0] == 200:
            general(
                f"Found {standard.tktcount} issue ticket(s) across {standard.pageqant} "
                f"page(s) in {qantrslt[2]} second(s)"
            )
            for indx in range(standard.pageqant):
                section(
                    f"Reading issue tickets information (Page {indx + 1} of {standard.pageqant})..."  # noqa: E501
                )
                pagerslt = moveobjc.iterpage(indx + 1)
                if pagerslt[0] == 200:
                    general(
                        f"Found {len(standard.pagerslt)} issue ticket(s) on this "
                        f"page in {pagerslt[2]} second(s)"
                    )
                    for jndx in standard.pagerslt:
                        callwait()
                        issurslt = moveobjc.itertkts(jndx)
                        section(
                            f"Migrating issue ticket {'with' if standard.movetags else 'without'} "  # noqa: E501
                            f"labels #{standard.issuiden} '{standard.issuname}' by "
                            f"'{standard.authname} (ID {standard.authorid})'..."
                        )
                        if issurslt[0] == 201:
                            general(f"Migrated to {issurslt[1]} in {issurslt[2]} second(s)")
                            if standard.movestat:
                                callwait()
                                section("Asserting issue ticket status...")
                                statrslt = moveobjc.iterstat()
                                if statrslt[0] == 200:
                                    general(
                                        f"Asserted CLOSE status of the ticket in {statrslt[2]} second(s)"  # noqa: E501
                                    )
                                elif statrslt[0] == 0:
                                    general(
                                        "Assertion unnecessary due to the OPEN status of the ticket"  # noqa: E501
                                    )
                                else:  # pragma: no cover
                                    # Tested already in `test_unit_itertkts`
                                    # From `test/test_unit_tkts`
                                    failure("Issue ticket status assertion failed!")
                                    general(
                                        f"Failed due to code '{statrslt[0]}' and reason '{statrslt[1]}' "  # noqa: E501
                                        f"in {statrslt[2]} second(s)"
                                    )
                            if standard.movecmts:
                                section("Reading comment information...")
                                standard.issucmts = jndx["comments"]
                                general(
                                    f"Found {len(standard.issucmts)} entities in 0.00 second(s)"
                                )
                                for kndx in standard.issucmts:
                                    callwait()
                                    cmtsrslt = moveobjc.itercmts(kndx)
                                    section(
                                        f"Transferring comment (Entity {standard.cmtsqant} of "
                                        f"{len(standard.issucmts)})..."
                                    )
                                    if cmtsrslt[0] == 201:
                                        general(
                                            f"Transferred to {cmtsrslt[1]} in {cmtsrslt[2]} second(s)"  # noqa: E501
                                        )
                                    else:  # pragma: no cover
                                        # Tested already in `test_unit_itercmts`
                                        # From `test/test_unit_tkts`
                                        failure("Comment transfer failed!")
                                        general(
                                            f"Failed due to code '{cmtsrslt[0]}' and reason '{cmtsrslt[1]}' "  # noqa: E501
                                            f"in {cmtsrslt[2]} second(s)"
                                        )
                                        sys.exit(1)
                                standard.cmtsqant = 0
                        else:  # pragma: no cover
                            # Tested already in `test_unit_itertkts`
                            # From `test/test_unit_tkts`
                            failure("Issue ticket migration failed!")
                            general(
                                f"Failed due to code '{issurslt[0]}' and reason '{issurslt[1]}' "
                                f"in {issurslt[2]} second(s)"
                            )
                else:  # pragma: no cover
                    # Tested already in `test_unit_iterpage`
                    # From `test/test_unit_tkts`
                    failure("Issue ticket information reading failed!")
                    general(
                        f"Failed due to code '{pagerslt[0]}' and reason '{pagerslt[1]}' in {pagerslt[2]} second(s)"  # noqa: E501
                    )
            success("Namespace assets transferring queue processed!")
            general(f"{standard.issutnfs} issue ticket(s) transferred")
            sys.exit(0)
        else:  # pragma: no cover
            # Tested already in `test_unit_getcount`
            # From `test/test_unit_tkts`
            failure("Source namespace issue ticket count failed!")
            general(
                f"Failed due to code '{qantrslt[0]}' and reason '{qantrslt[1]}' in {qantrslt[2]} second(s)"  # noqa: E501
            )
            sys.exit(1)
    else:
        for indx in standard.tktgroup:
            tkidrslt = moveobjc.iteriden(indx)
            section(f"Probing issue ticket #{indx}...")
            if tkidrslt[0] == 200:
                if not tkidrslt[1]:
                    general(f"Information retrieved in {tkidrslt[2]} second(s)")
                    callwait()
                    issurslt = moveobjc.itertkts(standard.issurslt)
                    section(
                        f"Migrating issue ticket {'with' if standard.movetags else 'without'} "
                        f"labels #{standard.issuiden} '{standard.issuname}' "
                        f"by '{standard.authname} (ID {standard.authorid})'..."
                    )
                    if issurslt[0] == 201:
                        general(f"Migrated to {issurslt[1]} in {issurslt[2]} second(s)")
                        if standard.movestat:
                            callwait()
                            section("Asserting issue ticket status...")
                            statrslt = moveobjc.iterstat()
                            if statrslt[0] == 200:
                                general(
                                    f"Asserted CLOSE status of the ticket in {statrslt[2]} second(s)"  # noqa: E501
                                )
                            elif statrslt[0] == 0:
                                general(
                                    "Assertion unnecessary due to the OPEN status of the ticket"
                                )
                            else:  # pragma: no cover
                                # Tested already in `test_unit_itertkts`
                                # From `test/test_unit_tkts`
                                failure("Issue ticket status assertion failed!")
                                general(
                                    f"Failed due to code '{statrslt[0]}' and reason '{statrslt[1]}' "  # noqa: E501
                                    f"      in {statrslt[2]} second(s)"
                                )
                        if standard.movecmts:
                            section("Reading comment information...")
                            standard.issucmts = standard.issurslt["comments"]
                            general(f"Found {len(standard.issucmts)} entities in 0.00 second(s)")
                            for kndx in standard.issucmts:
                                callwait()
                                cmtsrslt = moveobjc.itercmts(kndx)
                                section(
                                    f"Transferring comment (Entity {standard.cmtsqant} of {len(standard.issucmts)})..."  # noqa: E501
                                )
                                if cmtsrslt[0] == 201:
                                    general(
                                        f"Transferred to {cmtsrslt[1]} in {cmtsrslt[2]} second(s)"
                                    )
                                else:  # pragma: no cover
                                    # Tested already in `test_unit_itercmts`
                                    # From `test/test_unit_tkts`
                                    failure("Comment transfer failed!")
                                    general(
                                        f"Failed due to code '{cmtsrslt[0]}' and reason '{cmtsrslt[1]}'"  # noqa: E501
                                        f" in {cmtsrslt[2]} second(s)"
                                    )
                                    sys.exit(1)
                            standard.cmtsqant = 0
                    else:  # pragma: no cover
                        # Tested already in `test_unit_iteriden`
                        # From `test/test_unit_tkts`
                        failure("Issue ticket migration failed!")
                        general(
                            f"Failed due to code '{issurslt[0]}' and reason '{issurslt[1]}' in {issurslt[2]} second(s)"  # noqa: E501
                        )
                else:
                    general(
                        "Skipping issue ticket as the issue ticket status does not match the provided status"  # noqa: E501
                    )
            else:  # pragma: no cover
                # Tested already in `test_unit_getcount`
                # From `test/test_unit_tkts`
                failure("Issue ticket probing failed!")
                general(
                    f"Failed due to code '{tkidrslt[0]}' and reason '{tkidrslt[1]}' in {tkidrslt[2]} second(s)"  # noqa: E501
                )
        success("Namespace assets transferring queue processed!")
        general(f"{standard.issutnfs} issue ticket(s) transferred")
        sys.exit(0)
