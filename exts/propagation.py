"""
Propagation extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


from io import BytesIO

import aiohttp
import cairosvg

import discord
import discord.ext.commands as commands

import common as cmn


class PropagationCog(commands.Cog):
    muf_url = "https://prop.kc2g.com/renders/current/mufd-normal-now.svg"
    fof2_url = "https://prop.kc2g.com/renders/current/fof2-normal-now.svg"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.command(name="mufmap", aliases=["muf"], category=cmn.cat.weather)
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

    @commands.command(name="fof2map", aliases=["fof2", "critfreq"], category=cmn.cat.weather)
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


def setup(bot: commands.Bot):
    bot.add_cog(PropagationCog(bot))
