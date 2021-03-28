"""
Propagation extension for qrm
---
Copyright (C) 2019-2020 classabbyamp, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


from io import BytesIO

import aiohttp
import cairosvg
from datetime import datetime

import discord
import discord.ext.commands as commands

import common as cmn


class PropagationCog(commands.Cog):
    muf_url = "https://prop.kc2g.com/renders/current/mufd-normal-now.svg"
    fof2_url = "https://prop.kc2g.com/renders/current/fof2-normal-now.svg"
    gl_baseurl = "https://www.fourmilab.ch/cgi-bin/uncgi/Earth?img=ETOPO1_day-m.evif&dynimg=y&opt=-p"
    n0nbh_sun_url = "http://www.hamqsl.com/solarsun.php"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.command(name="mufmap", aliases=["muf"], category=cmn.Cats.WEATHER)
    async def mufmap(self, ctx: commands.Context):
        """Shows a world map of the Maximum Usable Frequency (MUF)."""
        async with ctx.typing():
            async with self.session.get(self.muf_url) as r:
                svg = await r.read()
            out = BytesIO(cairosvg.svg2png(bytestring=svg))
            file = discord.File(out, "muf_map.png")
            embed = cmn.embed_factory(ctx)
            embed.title = "Maximum Usable Frequency Map"
            embed.description = "Image from [prop.kc2g.com](https://prop.kc2g.com/)\nData sources listed on the page."
            embed.set_image(url="attachment://muf_map.png")
            await ctx.send(file=file, embed=embed)

    @commands.command(name="fof2map", aliases=["fof2", "critfreq"], category=cmn.Cats.WEATHER)
    async def fof2map(self, ctx: commands.Context):
        """Shows a world map of the Critical Frequency (foF2)."""
        async with ctx.typing():
            async with self.session.get(self.fof2_url) as r:
                svg = await r.read()
            out = BytesIO(cairosvg.svg2png(bytestring=svg))
            file = discord.File(out, "fof2_map.png")
            embed = cmn.embed_factory(ctx)
            embed.title = "Critical Frequency (foF2) Map"
            embed.description = "Image from [prop.kc2g.com](https://prop.kc2g.com/)\nData sources listed on the page."
            embed.set_image(url="attachment://fof2_map.png")
            await ctx.send(file=file, embed=embed)

    @commands.command(name="grayline", aliases=["greyline", "grey", "gray", "gl"], category=cmn.Cats.WEATHER)
    async def grayline(self, ctx: commands.Context):
        """Gets a map of the current greyline, where HF propagation is the best."""
        embed = cmn.embed_factory(ctx)
        embed.title = "Current Greyline Conditions"
        embed.colour = cmn.colours.good
        date_params = f"&date=1&utc={datetime.utcnow():%Y-%m-%d+%H:%M:%S}"
        embed.set_image(url=self.gl_baseurl + date_params)
        await ctx.send(embed=embed)

    @commands.command(name="solarweather", aliases=["solar", "bandconditions", "cond", "condx", "conditions"],
                      category=cmn.Cats.WEATHER)
    async def solarweather(self, ctx: commands.Context):
        """Gets a solar weather report."""
        embed = cmn.embed_factory(ctx)
        embed.title = "☀️ Current Solar Weather"
        if ctx.invoked_with in ["bandconditions", "cond", "condx", "conditions"]:
            embed.add_field(name="⚠️ Deprecated Command Alias",
                            value=(f"This command has been renamed to `{ctx.prefix}solar`!\n"
                                   "The alias you used will be removed in the next version."))
        embed.colour = cmn.colours.good
        embed.set_image(url=self.n0nbh_sun_url)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(PropagationCog(bot))
