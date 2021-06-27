"""
Wrapper to handle aiohttp connector creation.
---
Copyright (C) 2020-2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


import aiohttp


async def new_connector(*args, **kwargs) -> aiohttp.TCPConnector:
    """*Yes, it's just a coro to instantiate a class.*"""
    return aiohttp.TCPConnector(*args, **kwargs)
