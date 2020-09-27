"""
Conversion extension for qrm
---
Copyright (C) 2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import discord.ext.commands as commands

import common as cmn
from utils import dbconv


class ConvCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="dbconv", aliases=["db"], category=cmn.cat.ref)
    async def _db_conv(self, ctx: commands.Context, value: float, unit1: str, unit2: str):
        """
        Convert between decibels and scalar values for voltage, power, and antenna gain.

        **Valid Units**
        *Voltage:* V, mV, µV, uV, dBV, dBmV, dBµV, dBuV
        *Power:* fW, mW, W, kW, dBf, dBm, dBW, dBk
        *Antenna Gain:* dBi, dBd, dBq
        """
        embed = cmn.embed_factory(ctx)
        convobj = dbconv.DbConverter(value, unit1, unit2)

        embed.title = f"{convobj.initial:.3g} {convobj.unit1} = {convobj.converted:.3g} {convobj.unit2}"
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ConvCog(bot))
