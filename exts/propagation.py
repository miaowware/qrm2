"""
Propagation extension for qrm
---
Copyright (C) 2019-2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


from datetime import datetime
from io import BytesIO

import cairosvg
import httpx

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
        self.httpx_client: httpx.AsyncClient = bot.qrm.httpx_client

    @commands.command(name="mufmap", aliases=["muf"], category=cmn.Cats.WEATHER)
    async def mufmap(self, ctx: commands.Context):
        """Shows a world map of the Maximum Usable Frequency (MUF)."""
        async with ctx.typing():
            resp = await self.httpx_client.get(self.muf_url)
            await resp.aclose()
            if resp.status_code != 200:
                raise cmn.BotHTTPError(resp)
            out = BytesIO(cairosvg.svg2png(bytestring=await resp.aread()))
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
            resp = await self.httpx_client.get(self.fof2_url)
            await resp.aclose()
            if resp.status_code != 200:
                raise cmn.BotHTTPError(resp)
            out = BytesIO(cairosvg.svg2png(bytestring=await resp.aread()))
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

    @commands.command(name="solarweather", aliases=["solar"], category=cmn.Cats.WEATHER)
    async def solarweather(self, ctx: commands.Context):
        """Gets a solar weather report."""
        resp = await self.httpx_client.get(self.n0nbh_sun_url)
        await resp.aclose()
        if resp.status_code != 200:
            raise cmn.BotHTTPError(resp)
        img = BytesIO(await resp.aread())
        file = discord.File(img, "solarweather.png")
        embed = cmn.embed_factory(ctx)
        embed.title = "☀️ Current Solar Weather"
        embed.colour = cmn.colours.good
        embed.set_image(url="attachment://solarweather.png")
        await ctx.send(file=file, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(PropagationCog(bot))
