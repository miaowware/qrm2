"""
Information about callsigns for the prefixes command in hamcog.
---
Copyright (C) 2019-2023 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


from dataclasses import dataclass

from .callsigninfos import (us, ca)


@dataclass
class CallsignInfoData:
    """Represents a country's callsign info"""
    title: str = ""
    desc: str = ""
    calls: str = ""
    emoji: str = ""


options = {
    "us": CallsignInfoData(us.title, us.desc, us.calls, us.emoji),
    "ca": CallsignInfoData(ca.title, ca.desc, ca.calls, ca.emoji),
}
