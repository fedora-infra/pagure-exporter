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
from ..work.stat import DataDest, DataSrce
from .dcrt import failure, general, section, success


def show_status():
    section("Requesting for source namespace metadata...")
    source_result = DataSrce().obtain_info()
    if source_result == (200, "OK"):
        success("Source namespace metadata acquisition succeeded!")
        general("Name: %s" % str(standard.metadata_srce["reponame"]))
        general("Identifier: %s" % str(standard.metadata_srce["identity"]))
        general(
            "Maintainer: {} (ID {})".format(
                str(standard.metadata_srce["maintain"]["fullname"]),
                str(standard.metadata_srce["maintain"]["username"]),
            )
        )
        general("Location: %s" % str(standard.metadata_srce["repolink"]))
        general("Address: %s" % str(standard.display_url_srce))
        general(
            "Created on: %s" % strftime("%c", localtime(int(standard.metadata_srce["makedate"])))
        )
        general(
            "Last modified on: %s"
            % strftime("%c", localtime(int(standard.metadata_srce["lastmode"])))
        )
        general("Tags: %s" % str(standard.metadata_srce["tagslist"]))
        destination_result = DataDest().obtain_info()
        section("Requesting for destination namespace metadata...")
        if destination_result == (200, "OK"):
            success("Destination namespace metadata acquisition succeeded!")
            general("Name: %s" % str(standard.metadata_dest["reponame"]))
            general("Identifier: %s" % str(standard.metadata_dest["identity"]))
            general(
                "Maintainer: {} (ID {})".format(
                    str(standard.metadata_dest["maintain"]["fullname"]),
                    str(standard.metadata_dest["maintain"]["username"]),
                )
            )
            general("Location: %s" % str(standard.metadata_dest["repolink"]))
            general("Address: %s" % str(standard.display_url_dest))
            general("Created on: %s" % str(standard.metadata_dest["makedate"]))
            general("Last modified on: %s" % str(standard.metadata_dest["lastmode"]))
            general("Tags: %s" % str(standard.metadata_dest["tagslist"]))
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
