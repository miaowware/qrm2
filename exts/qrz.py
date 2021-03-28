"""
QRZ extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


from typing import Dict
from datetime import datetime

import aiohttp
from qrztools import qrztools, QrzAsync, QrzError
from gridtools import Grid, LatLong

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
                self.qrz = QrzAsync(keys.qrz_user, keys.qrz_pass, useragent="discord-qrm2",
                                    session=aiohttp.ClientSession(connector=bot.qrm.connector))
                # seed the qrz object with the previous session key, in case it already works
                try:
                    with open("data/qrz_session") as qrz_file:
                        self.qrz.session_key = qrz_file.readline().strip()
                except FileNotFoundError:
                    pass
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
                data = await self.qrz.get_callsign(callsign)
            except QrzError as e:
                embed.colour = cmn.colours.bad
                embed.description = str(e)
                await ctx.send(embed=embed)
                return

            embed.title = f"QRZ Data for {data.call}"
            embed.colour = cmn.colours.good
            embed.url = data.url
            if data.image != qrztools.QrzImage():
                embed.set_thumbnail(url=data.image.url)

            for title, val in qrz_process_info(data).items():
                if val is not None:
                    embed.add_field(name=title, value=val, inline=True)
            await ctx.send(embed=embed)


def qrz_process_info(data: qrztools.QrzCallsignData) -> Dict:
    if data.name != qrztools.Name():
        if opt.qrz_only_nickname:
            if data.name.nickname:
                name = data.name.nickname + " " + data.name.name
            elif data.name.first:
                name = data.name.first + " " + data.name.name
            else:
                name = data.name.name
        else:
            name = data.name.formatted_name
    else:
        name = None

    if data.address != qrztools.Address():
        state = ", " + data.address.state + " " if data.address.state else ""
        address = "\n".join([data.address.attn, data.address.line1, data.address.line2 + state, data.address.zip])
    else:
        address = None

    return {
        "Name": name,
        "Country": data.address.country,
        "Address": address,
        "Grid Square": data.grid if data.grid != Grid(LatLong(0, 0)) else None,
        "County": data.county if data.county else None,
        "CQ Zone": data.cq_zone if data.cq_zone else None,
        "ITU Zone": data.itu_zone if data.itu_zone else None,
        "IOTA Designator": data.iota if data.iota else None,
        "Expires": f"{data.expire_date:%Y-%m-%d}" if data.expire_date != datetime.min else None,
        "Aliases": ", ".join(data.aliases) if data.aliases else None,
        "Previous Callsign": data.prev_call if data.prev_call else None,
        "License Class": data.lic_class if data.lic_class else None,
        "Trustee": data.trustee if data.trustee else None,
        "eQSL?": "Yes" if data.eqsl else "No",
        "Paper QSL?": "Yes" if data.mail_qsl else "No",
        "LotW?": "Yes" if data.lotw_qsl else "No",
        "QSL Info": data.qsl_manager if data.qsl_manager else None,
        "Born": f"{data.born:%Y-%m-%d}" if data.born != datetime.min else None
    }


def setup(bot):
    bot.add_cog(QRZCog(bot))
