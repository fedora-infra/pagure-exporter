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
from ..work.tkts import MoveTickets
from .dcrt import failure, general, section, success, warning


def show_tickets():
    movetickets_obj = MoveTickets()
    section("Attempting source namespace issue ticket count...")
    warning(
        f"Extracting {'all ' if standard.ticket_state == 'open' or standard.ticket_state == 'closed' else ''}"  # noqa: E501
        f"{standard.ticket_state} issue tickets "
        f"{'with' if standard.move_labels else 'without'} labels, "
        f"{'with' if standard.move_state else 'without'} states, "
        f"{'with' if standard.move_secret else 'without'} privacy, "
        f"{'with' if standard.move_comments else 'without'} comments and "
        f"{'with' if standard.move_sequence else 'without'} order "
        f"off the given selection"
    )
    if not standard.ticket_group:
        ticket_count_result = movetickets_obj.get_ticket_count()
        if ticket_count_result[0] == 200:
            general(
                f"Found {standard.ticket_count} issue ticket(s) across {standard.page_index} "
                f"page(s) in {ticket_count_result[2]} second(s)"
            )
            for page_quantity_index in range(standard.page_index):
                section(
                    f"Reading issue tickets information (Page {page_quantity_index + 1} of {standard.page_index})..."  # noqa: E501
                )
                page_result = movetickets_obj.iterate_page(page_quantity_index + 1)
                if page_result[0] == 200:
                    general(
                        f"Found {len(standard.page_result)} issue ticket(s) on this "
                        f"page in {page_result[2]} second(s)"
                    )
                    for page in standard.page_result:
                        ticket_result = movetickets_obj.iterate_tickets(page)
                        section(
                            f"Migrating issue ticket {'with' if standard.move_labels else 'without'} "  # noqa: E501
                            f"labels #{standard.ticket_identity} '{standard.ticket_name}' by "
                            f"'{standard.author_name} (ID {standard.author_id})'..."
                        )
                        if ticket_result[0] == 201:
                            general(
                                f"Migrated to {ticket_result[1]} in {ticket_result[2]} second(s)"
                            )
                            if standard.move_state:
                                section("Asserting issue ticket status...")
                                ticket_status_result = movetickets_obj.iterate_ticket_status()
                                if ticket_status_result[0] == 200:
                                    general(
                                        f"Asserted CLOSE status of the ticket in {ticket_status_result[2]} second(s)"  # noqa: E501
                                    )
                                elif ticket_status_result[0] == 0:
                                    general(
                                        "Assertion unnecessary due to the OPEN status of the ticket"  # noqa: E501
                                    )
                                else:  # pragma: no cover
                                    # Tested already in `test_unit_itertkts`
                                    # From `test/test_unit_tkts`
                                    failure("Issue ticket status assertion failed!")
                                    general(
                                        f"Failed due to code '{ticket_status_result[0]}' and reason '{ticket_status_result[1]}' "  # noqa: E501
                                        f"in {ticket_status_result[2]} second(s)"
                                    )
                            if standard.move_comments:
                                section("Reading comment information...")
                                standard.ticket_comments = page["comments"]
                                general(
                                    f"Found {len(standard.ticket_comments)} entities in 0.00 second(s)"  # noqa: E501
                                )
                                for issue_comment in standard.ticket_comments:
                                    comment_result = movetickets_obj.iterate_comments(issue_comment)
                                    section(
                                        f"Transferring comment (Entity {standard.comment_quantity} of "  # noqa: E501
                                        f"{len(standard.ticket_comments)})..."
                                    )
                                    if comment_result[0] == 201:
                                        general(
                                            f"Transferred to {comment_result[1]} in {comment_result[2]} second(s)"  # noqa: E501
                                        )
                                    else:  # pragma: no cover
                                        # Tested already in `test_unit_itercmts`
                                        # From `test/test_unit_tkts`
                                        failure("Comment transfer failed!")
                                        general(
                                            f"Failed due to code '{comment_result[0]}' and reason '{comment_result[1]}' "  # noqa: E501
                                            f"in {comment_result[2]} second(s)"
                                        )
                                        sys.exit(1)
                                standard.comment_quantity = 0
                        else:  # pragma: no cover
                            # Tested already in `test_unit_itertkts`
                            # From `test/test_unit_tkts`
                            failure("Issue ticket migration failed!")
                            general(
                                f"Failed due to code '{ticket_result[0]}' and reason '{ticket_result[1]}' "  # noqa: E501
                                f"in {ticket_result[2]} second(s)"
                            )
                else:  # pragma: no cover
                    # Tested already in `test_unit_iterpage`
                    # From `test/test_unit_tkts`
                    failure("Issue ticket information reading failed!")
                    general(
                        f"Failed due to code '{page_result[0]}' and reason '{page_result[1]}' in {page_result[2]} second(s)"  # noqa: E501
                    )
            success("Namespace assets transferring queue processed!")
            general(f"{standard.issues_transferred} issue ticket(s) transferred")
            sys.exit(0)
        else:  # pragma: no cover
            # Tested already in `test_unit_getcount`
            # From `test/test_unit_tkts`
            failure("Source namespace issue ticket count failed!")
            general(
                f"Failed due to code '{ticket_count_result[0]}' and reason '{ticket_count_result[1]}' in {ticket_count_result[2]} second(s)"  # noqa: E501
            )
            sys.exit(1)
    else:
        for ticket_group in standard.ticket_group:
            ticket_by_id_result = movetickets_obj.iterate_ticket_by_id(ticket_group)
            section(f"Probing issue ticket #{ticket_group}...")
            if ticket_by_id_result[0] == 200:
                if not ticket_by_id_result[1]:
                    general(f"Information retrieved in {ticket_by_id_result[2]} second(s)")
                    ticket_result = movetickets_obj.iterate_tickets(standard.ticket_result)
                    section(
                        f"Migrating issue ticket {'with' if standard.move_labels else 'without'} "
                        f"labels #{standard.ticket_identity} '{standard.ticket_name}' "
                        f"by '{standard.author_name} (ID {standard.author_id})'..."
                    )
                    if ticket_result[0] == 201:
                        general(f"Migrated to {ticket_result[1]} in {ticket_result[2]} second(s)")
                        if standard.move_state:
                            section("Asserting issue ticket status...")
                            ticket_status_result = movetickets_obj.iterate_ticket_status()
                            if ticket_status_result[0] == 200:
                                general(
                                    f"Asserted CLOSE status of the ticket in {ticket_status_result[2]} second(s)"  # noqa: E501
                                )
                            elif ticket_status_result[0] == 0:
                                general(
                                    "Assertion unnecessary due to the OPEN status of the ticket"
                                )
                            else:  # pragma: no cover
                                # Tested already in `test_unit_itertkts`
                                # From `test/test_unit_tkts`
                                failure("Issue ticket status assertion failed!")
                                general(
                                    f"Failed due to code '{ticket_status_result[0]}' and reason '{ticket_status_result[1]}' "  # noqa: E501
                                    f"      in {ticket_status_result[2]} second(s)"
                                )
                        if standard.move_comments:
                            section("Reading comment information...")
                            standard.ticket_comments = standard.ticket_result["comments"]
                            general(
                                f"Found {len(standard.ticket_comments)} entities in 0.00 second(s)"
                            )
                            for issue_comment in standard.ticket_comments:
                                comment_result = movetickets_obj.iterate_comments(issue_comment)
                                section(
                                    f"Transferring comment (Entity {standard.comment_quantity} of {len(standard.ticket_comments)})..."  # noqa: E501
                                )
                                if comment_result[0] == 201:
                                    general(
                                        f"Transferred to {comment_result[1]} in {comment_result[2]} second(s)"  # noqa: E501
                                    )
                                else:  # pragma: no cover
                                    # Tested already in `test_unit_iterate_comments`
                                    # From `test/test_unit_tkts`
                                    failure("Comment transfer failed!")
                                    general(
                                        f"Failed due to code '{comment_result[0]}' and reason '{comment_result[1]}'"  # noqa: E501
                                        f" in {comment_result[2]} second(s)"
                                    )
                                    sys.exit(1)
                            standard.comment_quantity = 0
                    else:  # pragma: no cover
                        # Tested already in `test_unit_iteriden`
                        # From `test/test_unit_tkts`
                        failure("Issue ticket migration failed!")
                        general(
                            f"Failed due to code '{ticket_result[0]}' and reason '{ticket_result[1]}' in {ticket_result[2]} second(s)"  # noqa: E501
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
                    f"Failed due to code '{ticket_by_id_result[0]}' and reason '{ticket_by_id_result[1]}' in {ticket_by_id_result[2]} second(s)"  # noqa: E501
                )
        success("Namespace assets transferring queue processed!")
        general(f"{standard.issues_transferred} issue ticket(s) transferred")
        sys.exit(0)
