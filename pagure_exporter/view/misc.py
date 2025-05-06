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


from .dcrt import general, warning


def transfer_progress(branch_name, index, total_branches, is_available):
    if is_available:
        general(
            "[%d/%d] Branch '%s' was transferred to the destination namespace"
            % (int(index), int(total_branches), str(branch_name))
        )
    else:
        general(
            "[%d/%d] Branch '%s' was not found in the source namespace"
            % (int(index), int(total_branches), str(branch_name))
        )


def transfer_warning(is_available, total_branches):
    if is_available:
        warning("Transferring %d requested branches" % int(total_branches))
    else:
        warning("Transferring %d available branches" % int(total_branches))
