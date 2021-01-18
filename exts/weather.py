"""
Weather extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import re

import discord.ext.commands as commands

import common as cmn


class WeatherCog(commands.Cog):
    wttr_units_regex = re.compile(r"\B-([cCfF])\b")

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["solar", "bandconditions", "cond", "condx", "conditions"], category=cmn.cat.weather)
    async def solarweather(self, ctx: commands.Context):
        """Gets a solar weather report."""
        embed = cmn.embed_factory(ctx)
        embed.title = "☀️ Current Solar Weather"
        if ctx.invoked_with in ["bandconditions", "cond", "condx", "conditions"]:
            embed.add_field(name="⚠️ Deprecated Command Alias",
                            value=(f"This command has been renamed to `{ctx.prefix}solar`!\n"
                                   "The alias you used will be removed in the next version."))
        embed.colour = cmn.colours.good
        embed.set_image(url="http://www.hamqsl.com/solarsun.php")
        await ctx.send(embed=embed)

    @commands.group(name="weather", aliases=["wttr"], case_insensitive=True, category=cmn.cat.weather)
    async def _weather_conditions(self, ctx: commands.Context):
        """Gets local weather conditions from [wttr.in](http://wttr.in/).

        *Supported location types:*
        city name: `paris`
        any location: `~Eiffel Tower`
        Unicode name of any location in any language: `Москва`
        airport code (3 letters): `muc`
        domain name `@stackoverflow.com`
        area codes: `12345`
        GPS coordinates: `-78.46,106.79`

        Add a `-c` or `-f` to use Celcius or Fahrenheit: `-c YSC`"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_weather_conditions.command(name="forecast", aliases=["fc", "future"], category=cmn.cat.weather)
    async def _weather_conditions_forecast(self, ctx: commands.Context, *, location: str):
        """Gets local weather forecast for the next three days from [wttr.in](http://wttr.in/).
        See help of the `weather` command for possible location types and options."""
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
        embed.set_image(url=f"http://wttr.in/{loc}_{units}pnFQ.png")
        await ctx.send(embed=embed)

    @_weather_conditions.command(name="now", aliases=["n"], category=cmn.cat.weather)
    async def _weather_conditions_now(self, ctx: commands.Context, *, location: str):
        """Gets current local weather conditions from [wttr.in](http://wttr.in/).
        See help of the `weather` command for possible location types and options."""
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
        embed.set_image(url=f"http://wttr.in/{loc}_0{units}pnFQ.png")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(WeatherCog(bot))
