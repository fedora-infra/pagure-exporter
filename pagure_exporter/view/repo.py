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


def show_branch_transfer(pushrepo_obj: PushRepo):
    section("Reading branches data from the locally cloned assets...")
    source_branch_result, destination_branch_result = (
        pushrepo_obj.get_source_branches(),
        pushrepo_obj.get_destination_branches(),
    )
    if source_branch_result[0] and destination_branch_result[0]:
        success("Branches data reading succeeded!")
        general(
            "Available in source namespace: %d branch(es)" % len(standard.available_branches_srce)
        )
        for branch in standard.available_branches_srce:
            general("  - (SRCE branch) %s" % str(branch))
        general(
            "Available in destination namespace: %d branch(es)"
            % len(standard.available_branches_dest)
        )
        for branch in standard.available_branches_dest:
            general("  - (DEST branch) %s" % str(branch))
        general("Requested for transferring: %d branch(es)" % len(standard.branches_to_copy))
        for branch in standard.branches_to_copy:
            general("  - (RQST branch) %s" % str(branch))
        section("Initializing namespace assets branch(es) transfer...")
        transfer_result = pushrepo_obj.transfer_branches()
        general(
            "Assets transferred: %d branch(es) completed, %d branch(es) requested"
            % (int(standard.branch_transfer_index), int(standard.branch_transfer_quantity))
        )
        general("Time taken: %s second(s)" % str(transfer_result[1]))
        if transfer_result[0]:
            if standard.branch_transfer_index == standard.branch_transfer_quantity:
                success("Namespace assets branch(es) transfer succeeded!")
                return 0
            elif 0 < standard.branch_transfer_index < standard.branch_transfer_quantity:
                warning("Namespace assets branch(es) transfer partially completed!")
                return 2
            else:  # pragma: no cover
                # Tested already in `test_unit_tnfsrepo`
                # From `test/test_unit_repo`
                failure("Namespace assets branch(es) transfer failed!")
                return 1
        else:  # pragma: no cover
            # Tested already in `test_unit_tnfsrepo`
            # From `test/test_unit_repo`
            failure("Namespace assets branch(es) transfer failed!")
            general("Exception occurred: %s" % str(transfer_result[1]))
            return 1
    else:  # pragma: no cover
        # Tested already in `test_unit_check_source_assets` and `test_unit_check_destination_assets`
        # From `test/test_unit_repo`
        failure("Branches data reading failed!")
        error_message = (
            str(source_branch_result[1])
            if not source_branch_result[0]
            else str(destination_branch_result[1])
        )
        general("Exception occurred: %s" % error_message)
        return 1


def show_tag_transfer(pushrepo_obj: PushRepo):
    section("Reading tags data from the locally cloned assets...")
    source_tag_result, destination_tag_result = (
        pushrepo_obj.get_source_tags(),
        pushrepo_obj.get_destination_tags(),
    )
    if source_tag_result[0] and destination_tag_result[0]:
        success("Tags data reading succeeded!")
        general("Available in source namespace: %d tag(s)" % len(standard.available_tags_srce))
        for tag in standard.available_tags_srce:
            general("  - (SRCE tag) %s" % str(tag))
        general("Available in destination namespace: %d tag(s)" % len(standard.available_tags_dest))
        for tag in standard.available_tags_dest:
            general("  - (DEST tag) %s" % str(tag))
        general("Requested for transferring: %d tag(s)" % len(standard.tags_to_copy))
        for tag in standard.tags_to_copy:
            general("  - (RQST tag) %s" % str(tag))
        section("Initializing namespace assets tag(s) transfer...")
        transfer_result = pushrepo_obj.transfer_tags()
        general(
            "Assets transferred: %d tag(s) completed, %d tag(s) requested"
            % (int(standard.tag_transfer_index), int(standard.tag_transfer_quantity))
        )
        general("Time taken: %s second(s)" % str(transfer_result[1]))
        if transfer_result[0]:
            if standard.tag_transfer_index == standard.tag_transfer_quantity:
                success("Namespace assets tag(s) transfer succeeded!")
                return 0
            elif 0 < standard.tag_transfer_index < standard.tag_transfer_quantity:
                warning("Namespace assets tag(s) transfer partially completed!")
                return 2
            else:  # pragma: no cover
                # Tested already in `test_unit_tnfsrepo`
                # From `test/test_unit_repo`
                failure("Namespace assets tag(s) transfer failed!")
                return 1
        else:  # pragma: no cover
            # Tested already in `test_unit_tnfsrepo`
            # From `test/test_unit_repo`
            failure("Namespace assets tag(s) transfer failed!")
            general("Exception occurred: %s" % str(transfer_result[1]))
            return 1
    else:  # pragma: no cover
        # Tested already in `test_unit_check_source_assets` and `test_unit_check_destination_assets`
        # From `test/test_unit_repo`
        failure("Tags data reading failed!")
        error_message = (
            str(source_tag_result[1])
            if not source_tag_result[0]
            else str(destination_tag_result[1])
        )
        general("Exception occurred: %s" % error_message)
        return 1


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
                branch_transfer_status = show_branch_transfer(pushrepo_obj=pushrepo_obj)
                tag_transfer_status = show_tag_transfer(pushrepo_obj=pushrepo_obj)
                if branch_transfer_status == 0 and tag_transfer_status == 0:
                    sys.exit(0)
                elif 1 in (branch_transfer_status, tag_transfer_status):
                    sys.exit(1)
                else:
                    sys.exit(2)
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
