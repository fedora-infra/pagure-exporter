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


import json

from yaml import safe_load

from . import ResponseDefinition


def transfer_cassette_to_response(path: str) -> list:
    """
    Transfer VCR.py cassette into Response Definitions
    """
    with open(path, encoding="utf-8") as file:
        cassette = safe_load(file)

    defs = []

    for activity in cassette.get("interactions", []):
        method = activity["request"]["method"]
        url = activity["request"]["uri"]
        status = activity["response"]["status"]["code"]
        content_type = "application/json"

        headers = activity["response"].get("headers", {})
        if "Content-Type" in headers and headers["Content-Type"]:
            content_type = headers["Content-Type"][0]

        body = activity["response"]["body"].get("string")
        json_body = None
        if body:
            try:
                json_body = json.loads(body)
            except (json.JSONDecodeError, TypeError):
                json_body = None

        defs.append(ResponseDefinition(
            method=method.upper(),
            url=url,
            json=json_body,
            status=status,
            content_type=content_type,
        ))

    return defs
