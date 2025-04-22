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


from click import style

from ..conf.standard import logger

PASS = style("[ PASS ]", fg="green", bold=True)
FAIL = style("[ FAIL ]", fg="red", bold=True)
WARN = style("[ WARN ]", fg="yellow", bold=True)
BUSY = style("[ BUSY ]", fg="magenta", bold=True)
STDS = "        "


def success(message):
    logger.info(PASS + " " + style(message, fg="green", bold=True))


def failure(message):
    logger.error(FAIL + " " + style(message, fg="red", bold=True))


def warning(message):
    logger.warning(WARN + " " + style(message, fg="yellow", bold=True))


def section(message):
    logger.info(BUSY + " " + style(message, fg="magenta", bold=True))


def general(message):
    logger.info(STDS + " " + message)


def conceal(message):
    return "".join("*" for _ in message)
