"""
Wrapper to handle aiohttp connector creation.
---
Copyright (C) 2020-2021 classabbyamp, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import aiohttp


async def new_connector(*args, **kwargs) -> aiohttp.TCPConnector:
    """*Yes, it's just a coro to instantiate a class.*"""
    return aiohttp.TCPConnector(*args, **kwargs)
