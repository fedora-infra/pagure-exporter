"""
Pagure Exporter
Copyright (C) 2022-2025 Akashdeep Dhar

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

from ..conf import standard
from ..work.repo import PushRepo
from .dcrt import failure, general, section, success, warning


def show_repo():
    try:
        section("Starting migration...")
        pushrepo_obj = PushRepo()
        section("Attempting source namespace assets clone...")
        source_clone_result = pushrepo_obj.clone_source_repo()
        if source_clone_result[0]:
            success("Source namespace assets clone succeeded!")
            general("Directory: %s" % str(standard.clone_path_srce))
            general("Time taken: %s second(s)" % str(source_clone_result[1]))
            section("Attempting destination namespace assets clone...")
            destination_clone_result = pushrepo_obj.clone_destination_repo()
            if destination_clone_result[0]:
                success("Destination namespace assets clone succeeded!")
                general("Directory: %s" % str(standard.clone_path_dest))
                general("Time taken: %s second(s)" % str(destination_clone_result[1]))
                section("Reading branches data from the locally cloned assets...")
                source_branch_result, destination_branch_result = (
                    pushrepo_obj.get_source_branches(),
                    pushrepo_obj.get_destination_branches(),
                )
                if source_branch_result[0] and destination_branch_result[0]:
                    success("Branches data reading succeeded!")
                    general(
                        "Available in source namespace: %d branch(es)"
                        % len(standard.available_branches_srce)
                    )
                    for branch in standard.available_branches_srce:
                        general("  - (SRCE branch) %s" % str(branch))
                    general(
                        "Available in destination namespace: %d branch(es)"
                        % len(standard.available_branches_dest)
                    )
                    for branch in standard.available_branches_dest:
                        general("  - (DEST branch) %s" % str(branch))
                    general(
                        "Requested for transferring: %d branch(es)" % len(standard.branches_to_copy)
                    )
                    for branch in standard.branches_to_copy:
                        general("  - (RQST branch) %s" % str(branch))
                    section("Initializing namespace assets transfer...")
                    transfer_result = pushrepo_obj.transfer_repo()
                    general(
                        "Assets transferred: %d branch(es) completed, %d branch(es) requested"
                        % (int(standard.transfer_index), int(standard.transfer_quantity))
                    )
                    general("Time taken: %s second(s)" % str(transfer_result[1]))
                    if transfer_result[0]:
                        if standard.transfer_index == standard.transfer_quantity:
                            success("Namespace assets transfer succeeded!")
                            sys.exit(0)
                        elif 0 < standard.transfer_index < standard.transfer_quantity:
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
                        general("Exception occurred: %s" % str(transfer_result[1]))
                        sys.exit(1)
                else:  # pragma: no cover
                    # Tested already in `test_unit_cbrcsrce` and `test_unit_cbrcdest`
                    # From `test/test_unit_repo`
                    failure("Branches data reading failed!")
                    error_message = (
                        str(source_branch_result[1])
                        if not source_branch_result[0]
                        else str(destination_branch_result[1])
                    )
                    general("Exception occurred: %s" % error_message)
                    sys.exit(1)
            else:  # pragma: no cover
                # Tested already in `test_unit_downdest`
                # From `test/test_unit_repo`
                failure("Destination namespace assets clone failed!")
                general("Exception occurred: %s" % str(destination_clone_result[1]))
                sys.exit(1)
        else:  # pragma: no cover
            # Tested already in `test_unit_downsrce`
            # From `test/test_unit_repo`
            failure("Source namespace assets clone failed!")
            general("Exception occurred: %s" % str(source_clone_result[1]))
            sys.exit(1)
    except Exception as expt:
        failure("Migration failed!")
        general("Exception occurred: %s" % str(expt))
        sys.exit(1)
