"""
Callsign Lookup extension for qrm
---
Copyright (C) 2019-2020 classabbyamp, 0x5c  (as qrz.py)
Copyright (C) 2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


from typing import Dict

import aiohttp
from callsignlookuptools import QrzAsyncClient, CallsignLookupError, CallsignData

from discord.ext import commands

import common as cmn

import data.options as opt
import data.keys as keys


class QRZCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.qrz = None
        try:
            if keys.qrz_user and keys.qrz_pass:
                # seed the qrz object with the previous session key, in case it already works
                session_key = ""
                try:
                    with open("data/qrz_session") as qrz_file:
                        session_key = qrz_file.readline().strip()
                except FileNotFoundError:
                    pass
                self.qrz = QrzAsyncClient(username=keys.qrz_user, password=keys.qrz_pass, useragent="discord-qrm2",
                                          session_key=session_key,
                                          session=aiohttp.ClientSession(connector=bot.qrm.connector))
        except AttributeError:
            pass

    @commands.command(name="call", aliases=["qrz"], category=cmn.Cats.LOOKUP)
    async def _qrz_lookup(self, ctx: commands.Context, callsign: str, *flags):
        """Looks up a callsign on [QRZ.com](https://www.qrz.com/). Add `--link` to only link the QRZ page."""
        flags = [f.lower() for f in flags]

        if self.qrz is None or "--link" in flags:
            if ctx.invoked_with == "qrz":
                await ctx.send("⚠️ **Deprecated Command Alias**\n"
                               f"This command has been renamed to `{ctx.prefix}call`!\n"
                               "This alias will be removed in the next version.")
            await ctx.send(f"http://qrz.com/db/{callsign}")
            return

        embed = cmn.embed_factory(ctx)
        embed.title = f"QRZ Data for {callsign.upper()}"

        if ctx.invoked_with == "qrz":
            embed.description = ("⚠️ **Deprecated Command Alias**\n"
                                 f"This command has been renamed to `{ctx.prefix}call`!\n"
                                 "This alias will be removed in the next version.")

        async with ctx.typing():
            try:
                data = await self.qrz.search(callsign)
            except CallsignLookupError as e:
                embed.colour = cmn.colours.bad
                embed.description = str(e)
                await ctx.send(embed=embed)
                return

            embed.title = f"QRZ Data for {data.callsign}"
            embed.colour = cmn.colours.good
            embed.url = data.url
            if data.image is not None:
                embed.set_thumbnail(url=data.image.url)

            for title, val in qrz_process_info(data).items():
                if val:
                    embed.add_field(name=title, value=val, inline=True)
            await ctx.send(embed=embed)


def qrz_process_info(data: CallsignData) -> Dict:
    if data.name is not None:
        if opt.qrz_only_nickname:
            nm = data.name.name if data.name.name is not None else ""
            if data.name.nickname is not None:
                name = data.name.nickname + " " + nm
            elif data.name.first:
                name = data.name.first + " " + nm
            else:
                name = nm
        else:
            name = str(data.name)
    else:
        name = None

    return {
        "Name": name,
        "Country": data.address.country if data.address is not None else None,
        "Address": str(data.address),
        "Grid Square": str(data.grid),
        "County": data.county,
        "CQ Zone": str(data.cq_zone),
        "ITU Zone": str(data.itu_zone),
        "IOTA Designator": data.iota,
        "Expires": f"{data.expire_date:%Y-%m-%d}" if data.expire_date is not None else None,
        "Aliases": ", ".join(data.aliases) if data.aliases else None,
        "Previous Callsign": data.prev_call,
        "License Class": str(data.lic_class),
        "Trustee": str(data.trustee),
        "eQSL?": data.qsl.eqsl.name.title() if data.qsl is not None else None,
        "Paper QSL?": data.qsl.mail.name.title() if data.qsl is not None else None,
        "LotW?": data.qsl.lotw.name.title() if data.qsl is not None else None,
        "QSL Info": str(data.qsl.info) if data.qsl is not None else None,
        "Born": f"{data.born:%Y-%m-%d}" if data.born is not None else None
    }


def setup(bot):
    bot.add_cog(QRZCog(bot))
