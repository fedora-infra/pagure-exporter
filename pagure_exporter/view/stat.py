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
from time import localtime, strftime

from ..conf import standard
from ..work.stat import DestinationData, SourceData
from .dcrt import failure, general, section, success


def show_status():
    section("Requesting for source namespace metadata...")
    source_result = SourceData().obtain_info()
    if source_result == (200, "OK"):
        success("Source namespace metadata acquisition succeeded!")
        general("Name: %s" % str(standard.source_metadata["reponame"]))
        general("Identifier: %s" % str(standard.source_metadata["identity"]))
        general(
            "Maintainer: {} (ID {})".format(
                str(standard.source_metadata["maintain"]["fullname"]),
                str(standard.source_metadata["maintain"]["username"]),
            )
        )
        general("Location: %s" % str(standard.source_metadata["repolink"]))
        general("Address: %s" % str(standard.source_display_url))
        general(
            "Created on: %s" % strftime("%c", localtime(int(standard.source_metadata["makedate"])))
        )
        general(
            "Last modified on: %s"
            % strftime("%c", localtime(int(standard.source_metadata["lastmode"])))
        )
        general("Tags: %s" % str(standard.source_metadata["tagslist"]))
        destination_result = DestinationData().obtain_info()
        section("Requesting for destination namespace metadata...")
        if destination_result == (200, "OK"):
            success("Destination namespace metadata acquisition succeeded!")
            general("Name: %s" % str(standard.destination_metadata["reponame"]))
            general("Identifier: %s" % str(standard.destination_metadata["identity"]))
            general(
                "Maintainer: {} (ID {})".format(
                    str(standard.destination_metadata["maintain"]["fullname"]),
                    str(standard.destination_metadata["maintain"]["username"]),
                )
            )
            general("Location: %s" % str(standard.destination_metadata["repolink"]))
            general("Address: %s" % str(standard.destination_display_url))
            general("Created on: %s" % str(standard.destination_metadata["makedate"]))
            general("Last modified on: %s" % str(standard.destination_metadata["lastmode"]))
            general("Tags: %s" % str(standard.destination_metadata["tagslist"]))
        else:
            failure("Destination namespace metadata acquisition failed!")
            general("The namespace metadata could not be acquired.")
            general("Code: %s" % str(destination_result[0]))
            general("Reason: %s" % str(destination_result[1]))
            sys.exit(1)
    else:
        failure("Source namespace metadata acquisition failed!")
        general("The namespace metadata could not be acquired.")
        general("Code: %s" % str(source_result[0]))
        general("Reason: %s" % str(source_result[1]))
        sys.exit(1)
