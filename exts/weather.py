"""
Weather extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""

import io
import re

import aiohttp

import discord
import discord.ext.commands as commands

import common as cmn


class WeatherCog(commands.Cog):
    wttr_units_regex = re.compile(r"\B-([cCfF])\b")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.command(name="bandconditions", aliases=["cond", "condx", "conditions"], category=cmn.cat.weather)
    async def _band_conditions(self, ctx: commands.Context):
        """Posts an image of HF Band Conditions."""
        async with ctx.typing():
            embed = cmn.embed_factory(ctx)
            embed.title = "Current Solar Conditions"
            embed.colour = cmn.colours.good
            async with self.session.get("http://www.hamqsl.com/solarsun.php") as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                data = io.BytesIO(await resp.read())
            embed.set_image(url=f"attachment://condx.png")
            await ctx.send(embed=embed, file=discord.File(data, "condx.png"))

    @commands.group(name="weather", aliases=["wttr"], category=cmn.cat.weather)
    async def _weather_conditions(self, ctx: commands.Context):
        """Posts an image of Local Weather Conditions from [wttr.in](http://wttr.in/).

*Supported location types:*
    city name: `paris`
    any location: `~Eiffel Tower`
    Unicode name of any location in any language: `Москва`
    airport code (3 letters): `muc`
    domain name `@stackoverflow.com`
    area codes: `12345`
    GPS coordinates: `-78.46,106.79`
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_weather_conditions.command(name="forecast", aliases=["fc", "future"], category=cmn.cat.weather)
    async def _weather_conditions_forecast(self, ctx: commands.Context, *, location: str):
        """Posts an image of Local Weather Conditions for the next three days from [wttr.in](http://wttr.in/).
See help for weather command for possible location types. Add a `-c` or `-f` to use Celcius or Fahrenheit."""
        async with ctx.typing():
            try:
                units_arg = re.search(self.wttr_units_regex, location).group(1)
            except AttributeError:
                units_arg = ""
            if units_arg.lower() == "f":
                units = "u"
            elif units_arg.lower() == "c":
                units = "m"
            else:
                units = ""

            loc = self.wttr_units_regex.sub("", location).strip()

            embed = cmn.embed_factory(ctx)
            embed.title = f"Weather Forecast for {loc}"
            embed.description = "Data from [wttr.in](http://wttr.in/)."
            embed.colour = cmn.colours.good

            loc = loc.replace(" ", "+")
            async with self.session.get(f"http://wttr.in/{loc}_{units}pnFQ.png") as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                data = io.BytesIO(await resp.read())
            embed.set_image(url=f"attachment://wttr_forecast.png")
            await ctx.send(embed=embed, file=discord.File(data, "wttr_forecast.png"))

    @_weather_conditions.command(name="now", aliases=["n"], category=cmn.cat.weather)
    async def _weather_conditions_now(self, ctx: commands.Context, *, location: str):
        """Posts an image of current Local Weather Conditions from [wttr.in](http://wttr.in/).
See help for weather command for possible location types. Add a `-c` or `-f` to use Celcius or Fahrenheit."""
        async with ctx.typing():
            try:
                units_arg = re.search(self.wttr_units_regex, location).group(1)
            except AttributeError:
                units_arg = ""
            if units_arg.lower() == "f":
                units = "u"
            elif units_arg.lower() == "c":
                units = "m"
            else:
                units = ""

            loc = self.wttr_units_regex.sub("", location).strip()

            embed = cmn.embed_factory(ctx)
            embed.title = f"Current Weather for {loc}"
            embed.description = "Data from [wttr.in](http://wttr.in/)."
            embed.colour = cmn.colours.good

            loc = loc.replace(" ", "+")
            async with self.session.get(f"http://wttr.in/{loc}_0{units}pnFQ.png") as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                data = io.BytesIO(await resp.read())
            embed.set_image(url=f"attachment://wttr_now.png")
            await ctx.send(embed=embed, file=discord.File(data, "wttr_now.png"))


def setup(bot: commands.Bot):
    bot.add_cog(WeatherCog(bot))
