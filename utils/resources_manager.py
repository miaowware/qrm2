"""
Resources manager for qrm2.
---
Copyright (C) 2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


from pathlib import Path

import requests

from utils.resources_models import Index


class ResourcesManager:
    def __init__(self, basedir: Path, url: str, versions: dict):
        self.basedir = basedir
        self.url = url
        self.versions = versions
        self.index: Index = self.sync_start(basedir)

    def parse_index(self, index: str):
        """Parses the index."""
        return Index.parse_raw(index)

    def sync_fetch(self, filepath: str):
        """Fetches files in sync mode."""
        self.print_msg(f"Fetching {filepath}", "sync")
        with requests.get(self.url + filepath) as resp:
            return resp.content

    def sync_start(self, basedir: Path) -> Index:
        """Takes cares of constructing the local resources repository and initialising the RM."""
        self.print_msg("Initialising ResourceManager", "sync")
        self.ensure_dir(basedir)
        try:
            raw = self.sync_fetch("index.json")
            new_index: Index = self.parse_index(raw)
            with (basedir / "index.json").open("wb") as file:
                file.write(raw)
        except (requests.RequestException, OSError) as ex:
            self.print_msg(f"There was an issue fetching the index: {ex.__class__.__name__}: {ex}", "sync")
            if (basedir / "index.json").exists():
                self.print_msg("Old file exist, using old resources", "fallback")
                with (basedir / "index.json").open("r") as file:
                    old_index = self.parse_index(file.read())
                for res, ver in self.versions.items():
                    for file in old_index[res][ver]:
                        if not (basedir / file.filename).exists():
                            self.print_msg(f"Error: {file.filename} is missing", "fallback")
                            raise SystemExit(1)
                return old_index
            raise SystemExit(1)
        for res, ver in self.versions.items():
            for file in new_index[res][ver]:
                try:
                    with (basedir / file.filename).open("wb") as f:
                        f.write(self.sync_fetch(file.filename))
                except (requests.RequestException, OSError) as ex:
                    ex_cls = ex.__class__.__name__
                    self.print_msg(f"There was an issue fetching {file.filename}: {ex_cls}: {ex}", "sync")
                    if not (basedir / file.filename).exists():
                        raise SystemExit(1)
                    self.print_msg("Old file exists, using it", "fallback")
        return new_index

    def ensure_dir(self, basedir: Path) -> bool:
        """Ensures that the resources/ directory is present. Creates as necessary."""
        if basedir.is_file():
            raise FileExistsError(f"'{basedir}' is not a directory!")
        if not basedir.exists():
            self.print_msg("Creating resources directory")
            basedir.mkdir()
            return True
        return False

    def print_msg(self, msg: str, mode: str = None):
        """Formats and prints messages for the resources manager."""
        message = "RM: "
        message += msg
        if mode:
            message += f" ({mode})"
        print(message)
