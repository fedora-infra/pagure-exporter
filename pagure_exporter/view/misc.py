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


from .dcrt import general, warning


def tnfsprog(brchname, indx, qant, avbl):
    if avbl:
        general(
            "[%d/%d] Branch '%s' was transferred to the destination namespace"
            % (int(indx), int(qant), str(brchname))
        )
    else:
        general(
            "[%d/%d] Branch '%s' was not found in the source namespace"
            % (int(indx), int(qant), str(brchname))
        )


def tnfswarn(avbl, qant):
    if avbl:
        warning("Transferring %d requested branches" % int(qant))
    else:
        warning("Transferring %d available branches" % int(qant))
