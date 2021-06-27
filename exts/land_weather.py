"""
Land Weather extension for qrm
---
Copyright (C) 2019-2020 classabbyamp, 0x5c  (as weather.py)
Copyright (C) 2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


import re
from typing import List

import aiohttp

from discord import Embed
import discord.ext.commands as commands

import common as cmn


class WeatherCog(commands.Cog):
    wttr_units_regex = re.compile(r"\B-([cCfF])\b")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.group(name="weather", aliases=["wttr"], case_insensitive=True, category=cmn.Cats.WEATHER)
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

    @_weather_conditions.command(name="forecast", aliases=["fc", "future"], category=cmn.Cats.WEATHER)
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

    @_weather_conditions.command(name="now", aliases=["n"], category=cmn.Cats.WEATHER)
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

    @commands.command(name="metar", category=cmn.Cats.WEATHER)
    async def metar(self, ctx: commands.Context, airport: str, hours: int = 0):
        """Gets current raw METAR (Meteorological Terminal Aviation Routine Weather Report) for an airport. \
        Optionally, a number of hours can be given to show a number of hours of historical METAR data.

        Airports should be given as an \
        [ICAO code](https://en.wikipedia.org/wiki/List_of_airports_by_IATA_and_ICAO_code)."""
        await ctx.send(embed=await self.gen_metar_taf_embed(ctx, airport, hours, False))

    @commands.command(name="taf", category=cmn.Cats.WEATHER)
    async def taf(self, ctx: commands.Context, airport: str):
        """Gets forecasted raw TAF (Terminal Aerodrome Forecast) data for an airport. Includes the latest METAR data.

        Airports should be given as an \
        [ICAO code](https://en.wikipedia.org/wiki/List_of_airports_by_IATA_and_ICAO_code)."""
        await ctx.send(embed=await self.gen_metar_taf_embed(ctx, airport, 0, True))

    async def gen_metar_taf_embed(self, ctx: commands.Context, airport: str, hours: int, taf: bool) -> Embed:
        embed = cmn.embed_factory(ctx)
        airport = airport.upper()

        if re.fullmatch(r"\w(\w|\d){2,3}", airport):
            metar = await self.get_metar_taf_data(airport, hours, taf)

            if taf:
                embed.title = f"Current TAF for {airport}"
            elif hours > 0:
                embed.title = f"METAR for {airport} for the last {hours} hour{'s' if hours > 1 else ''}"
            else:
                embed.title = f"Current METAR for {airport}"

            embed.description = "Data from [aviationweather.gov](https://www.aviationweather.gov/metar/data)."
            embed.colour = cmn.colours.good

            data = "\n".join(metar)
            embed.description += f"\n\n```\n{data}\n```"
        else:
            embed.title = "Invalid airport given!"
            embed.colour = cmn.colours.bad
        return embed

    async def get_metar_taf_data(self, airport: str, hours: int, taf: bool) -> List[str]:
        url = (f"https://www.aviationweather.gov/metar/data?ids={airport}&format=raw&hours={hours}"
               f"&taf={'on' if taf else 'off'}&layout=off")
        async with self.session.get(url) as r:
            if r.status != 200:
                raise cmn.BotHTTPError(r)
            page = await r.text()

        # pare down to just the data
        page = page.split("<!-- Data starts here -->")[1].split("<!-- Data ends here -->")[0].strip()
        # split at <hr>s
        data = re.split(r"<hr.*>", page, maxsplit=len(airport))

        parsed = []
        for sec in data:
            if sec.strip():
                for line in sec.split("\n"):
                    line = line.strip()
                    # remove HTML stuff
                    line = line.replace("<code>", "").replace("</code>", "")
                    line = line.replace("<strong>", "").replace("</strong>", "")
                    line = line.replace("<br/>", "\n").replace("&nbsp;", " ")
                    line = line.strip("\n")
                    parsed.append(line)
        return parsed


def setup(bot: commands.Bot):
    bot.add_cog(WeatherCog(bot))
