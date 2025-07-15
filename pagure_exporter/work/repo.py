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


import os
import time
from tempfile import TemporaryDirectory

from git import Repo

from ..conf import standard
from ..view.misc import transfer_progress, transfer_warning


class PushRepo:
    def __init__(self):
        self.clone_url_srce = standard.clone_url_srce
        self.clone_url_dest = standard.clone_url_dest
        self.pagure_token = standard.pagure_token
        self.gitlab_token = standard.gitlab_token
        self.branches_to_copy = standard.branches_to_copy
        self.source_args = dict(prefix=standard.temp_prefix_srce, dir=standard.temp_dir)
        self.destination_args = dict(prefix=standard.temp_prefix_dest, dir=standard.temp_dir)
        self.source_location = TemporaryDirectory(**self.source_args)
        self.destination_location = TemporaryDirectory(**self.destination_args)
        standard.clone_path_srce = self.source_location.name
        standard.clone_path_dest = self.destination_location.name

    def clone_source_repo(self):
        try:
            start_time = time.time()
            repo_obj = Repo.clone_from(url=self.clone_url_srce, to_path=self.source_location.name)
            repo_obj.remote(standard.default_remote).fetch(tags=True)
            stop_time = time.time()
            return True, "%.2f" % (stop_time - start_time)
        except Exception as expt:
            return False, str(expt)

    def clone_destination_repo(self):
        try:
            start_time = time.time()
            repo_obj = Repo.clone_from(
                url=self.clone_url_dest, to_path=self.destination_location.name
            )
            repo_obj.remote(standard.default_remote).fetch(tags=True)
            stop_time = time.time()
            return True, "%.2f" % (stop_time - start_time)
        except Exception as expt:
            return False, str(expt)

    def get_source_branches(self):
        if os.path.exists(os.path.join(self.source_location.name, ".git")):
            repo_obj = Repo(path=self.source_location.name)
            branch_list = [
                refx.name.replace("%s/" % standard.default_remote, "")
                for refx in repo_obj.remote(standard.default_remote).refs
            ]
            standard.available_branches_srce = list(branch_list)
            return True, branch_list
        else:
            return False, "Cloned source namespace assets could not be found"

    def get_source_tags(self):
        if os.path.exists(os.path.join(self.source_location.name, ".git")):
            repo_obj = Repo(path=self.source_location.name)
            tag_list = [tag.name for tag in repo_obj.tags]
            standard.available_tags_srce = list(tag_list)
            return True, tag_list
        else:
            return False, "Cloned source namespace assets could not be found"

    def get_destination_branches(self):
        if os.path.exists(os.path.join(self.destination_location.name, ".git")):
            repo_obj = Repo(path=self.destination_location.name)
            branch_list = [
                refx.name.replace("%s/" % standard.default_remote, "")
                for refx in repo_obj.remote(standard.default_remote).refs
            ]
            standard.available_branches_dest = list(branch_list)
            return True, branch_list
        else:
            return False, "Cloned destination namespace assets could not be found"

    def get_destination_tags(self):
        if os.path.exists(os.path.join(self.destination_location.name, ".git")):
            repo_obj = Repo(path=self.destination_location.name)
            tag_list = [tag.name for tag in repo_obj.tags]
            standard.available_tags_dest = list(tag_list)
            return True, tag_list
        else:
            return False, "Cloned source namespace assets could not be found"

    def transfer_branches(self):
        if os.path.exists(os.path.join(self.source_location.name, ".git")):
            start_time = time.time()
            repo_obj = Repo(path=self.source_location.name)
            repo_obj.create_remote(standard.new_remote, url=standard.clone_url_dest)
            if len(standard.branches_to_copy) == 0:
                standard.branch_transfer_quantity = len(standard.available_branches_srce)
                transfer_warning("branch", False, standard.branch_transfer_quantity)
                for brdx in standard.available_branches_srce:
                    repo_obj.git.checkout("%s" % brdx)
                    repo_obj.git.push(standard.new_remote, "--set-upstream", brdx, "--force")
                    transfer_progress(
                        "branch",
                        brdx,
                        standard.available_branches_srce.index(brdx) + 1,
                        len(standard.available_branches_srce),
                        True,
                    )
                    standard.branch_transfer_index += 1
            else:
                standard.branch_transfer_quantity = len(standard.branches_to_copy)
                transfer_warning("branch", True, standard.branch_transfer_quantity)
                for brdx in standard.branches_to_copy:
                    if brdx in standard.available_branches_srce:
                        repo_obj.git.checkout("%s" % brdx)
                        repo_obj.git.push(standard.new_remote, "--set-upstream", brdx, "--force")
                        transfer_progress(
                            "branch",
                            brdx,
                            standard.branches_to_copy.index(brdx) + 1,
                            len(standard.branches_to_copy),
                            True,
                        )
                        standard.branch_transfer_index += 1
                    else:
                        transfer_progress(
                            "branch",
                            brdx,
                            standard.branches_to_copy.index(brdx) + 1,
                            len(standard.branches_to_copy),
                            False,
                        )
            stop_time = time.time()
            return True, "%.2f" % (stop_time - start_time)
        else:
            return False, "Cloned namespace assets could not be found"

    def transfer_tags(self):
        if os.path.exists(os.path.join(self.source_location.name, ".git")):
            start_time = time.time()
            repo_obj = Repo(path=self.source_location.name)
            if len(standard.tags_to_copy) == 0:
                standard.tag_transfer_quantity = len(standard.available_tags_srce)
                transfer_warning("tag", False, standard.tag_transfer_quantity)
                for tag in standard.available_tags_srce:
                    repo_obj.git.push(standard.new_remote, tag, force=True)
                    transfer_progress(
                        "tag",
                        tag,
                        standard.available_tags_srce.index(tag) + 1,
                        len(standard.available_tags_srce),
                        True,
                    )
                    standard.tag_transfer_index += 1
            else:
                standard.tag_transfer_quantity = len(standard.tags_to_copy)
                transfer_warning("tag", True, standard.tag_transfer_quantity)
                for tag in standard.tags_to_copy:
                    if tag in standard.available_tags_srce:
                        repo_obj.git.push(standard.new_remote, tag, force=True)
                        transfer_progress(
                            "tag",
                            tag,
                            standard.tags_to_copy.index(tag) + 1,
                            len(standard.tags_to_copy),
                            True,
                        )
                        standard.tag_transfer_index += 1
                    else:
                        transfer_progress(
                            "tag",
                            tag,
                            standard.tags_to_copy.index(tag) + 1,
                            len(standard.tags_to_copy),
                            False,
                        )
            stop_time = time.time()
            return True, "%.2f" % (stop_time - start_time)
        else:
            return False, "Cloned namespace assets could not be found"
