"""
Resource index models for qrm2.
---
Copyright (C) 2021-2023 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


from collections.abc import Mapping
from datetime import datetime

from pydantic import BaseModel, RootModel


class File(BaseModel):
    filename: str
    hash: str

    # For some reason those were not the same???
    def __str__(self) -> str:
        return repr(self)


class Resource(RootModel, Mapping):
    root: dict[str, list[File]]

    def __getitem__(self, key: str) -> list[File]:
        return self.root[key]

    def __iter__(self):
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)

    # For some reason those were not the same???
    def __str__(self) -> str:
        return repr(self)

    # Make the repr more logical (despite the technical inaccuracy)
    def __repr_args__(self):
        return self.root.items()


class Index(BaseModel, Mapping):
    last_updated: datetime
    resources: dict[str, Resource]

    def __getitem__(self, key: str) -> Resource:
        return self.resources[key]

    def __iter__(self):
        return iter(self.resources)

    def __len__(self) -> int:
        return len(self.resources)

    # For some reason those were not the same???
    def __str__(self) -> str:
        return repr(self)
