"""
Information about callsigns for the prefixes command in hamcog.
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of
the GNU General Public License, version 2.
"""

from .callsigninfos import (us, ca)
from common import CallsignInfoData


# format: country: (title, description, text)
options = {
    "us": CallsignInfoData([us.title, us.desc, us.calls, us.emoji]),
    "ca": CallsignInfoData([ca.title, ca.desc, ca.calls, ca.emoji]),
}
