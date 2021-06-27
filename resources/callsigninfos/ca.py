"""
Information about callsigns for the CA prefixes command in hamcog.
---
Copyright (C) 2019-2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


title = "Canadian Callsign Rules"
emoji = "🇨🇦"
desc = ("Canadian operators are limited to callsigns with the prefixes of their address' province/territory. "
        "Initially, operators can choose a callsign with a 3-letter suffix. "
        "Later on, they can apply to change or for additional callsigns. "
        "Operators can only hold one 2-letter suffix callsign, but many 3-letter suffix callsigns. "
        "If the number of 2-letter suffix callsigns exceeds 80% of the total available, "
        "operators can only choose a 2-letter suffix after holding a license for 5 years. "
        "If the operator is a family member of a deceased operator, they are not bound by this restriction. "
        "Data from [ISED Canada (RIC-9)](https://www.ic.gc.ca/eic/site/smt-gst.nsf/eng/sf02102.html).")
calls = {
    "Provinces": (
        "**Nova Scotia:** VE1 and VA1\n"
        "**Québec:** VE2 and VA2\n"
        "**Ontario:** VE3 and VA3\n"
        "**Manitoba:** VE4 and VA4\n"
        "**Saskatchewan:** VE5 and VA5\n"
        "**Alberta:** VE6 and VA6\n"
        "**British Columbia:** VE7 and VA7\n"
        "**New Brunswick:** VE9\n"
        "**Newfoundland:** VO1\n"
        "**Labrador:** VO2\n"
        "**Prince Edward Island:** VY2\n"
    ),
    "Territories": (
        "**Northwest Territories:** VE8\n"
        "**Nunavut:** VY0\n"
        "**Yukon:** VY1\n"
    ),
    "Other": (
        "**International Waters:** VE0\n"
        "**Government of Canada:** VY9\n"
        "**Sable Island:** CY0\n"
        "**St-Paul Island:** CY9\n"
    ),
    "Special Event": "Various prefixes in the ranges: CF-CK, CY-CZ, VA-VG, VO, VX-VY, XJ-XO"
}
