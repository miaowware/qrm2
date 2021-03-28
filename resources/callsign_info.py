"""
Information about callsigns for the prefixes command in hamcog.
---
Copyright (C) 2019-2020 classabbyamp, 0x5c

This file is part of discord-qrmbot and is released under the terms of
the GNU General Public License, version 2.
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
