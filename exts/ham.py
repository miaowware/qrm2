"""
Ham extension for qrm
---
Copyright (C) 2019-2021 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import json
from datetime import datetime

import discord.ext.commands as commands

import common as cmn
from resources import callsign_info


class HamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pfxs = callsign_info.options
        with open(cmn.paths.resources / "phonetics.1.json") as file:
            d = json.load(file)
            self.phonetics: dict[str, str] = d["phonetics"]
            self.pweights: dict[str, int] = d["pweights"]
        with open(cmn.paths.resources / "qcodes.1.json") as file:
            self.qcodes: dict = json.load(file)

    @commands.command(name="qcode", aliases=["q"], category=cmn.Cats.REF)
    async def _qcode_lookup(self, ctx: commands.Context, qcode: str):
        """Looks up the meaning of a Q Code."""
        qcode = qcode.upper()
        embed = cmn.embed_factory(ctx)
        if qcode in self.qcodes:
            embed.title = qcode
            embed.description = self.qcodes[qcode]
            embed.colour = cmn.colours.good
        else:
            embed.title = f"Q Code {qcode} not found"
            embed.colour = cmn.colours.bad
        await ctx.send(embed=embed)

    @commands.command(name="phonetics", aliases=["ph", "phoneticize", "phoneticise", "phone"], category=cmn.Cats.REF)
    async def _phonetics_lookup(self, ctx: commands.Context, *, msg: str):
        """Returns NATO phonetics for a word or phrase."""
        result = ""
        for char in msg.lower():
            if char.isalpha():
                result += self.phonetics[char]
            else:
                result += char
            result += " "
        embed = cmn.embed_factory(ctx)
        embed.title = f"Phonetics for {msg}"
        embed.description = result.title()
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="utc", aliases=["z"], category=cmn.Cats.REF)
    async def _utc_lookup(self, ctx: commands.Context):
        """Returns the current time in UTC."""
        now = datetime.utcnow()
        result = "**" + now.strftime("%Y-%m-%d %H:%M") + "Z**"
        embed = cmn.embed_factory(ctx)
        embed.title = "The current time is:"
        embed.description = result
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="prefixes", aliases=["vanity", "pfx", "vanities", "prefix"], category=cmn.Cats.REF)
    async def _vanity_prefixes(self, ctx: commands.Context, country: str = ""):
        """Lists valid callsign prefixes for different countries."""
        country = country.lower()
        embed = cmn.embed_factory(ctx)
        if country not in self.pfxs:
            desc = "Possible arguments are:\n"
            for key, val in self.pfxs.items():
                desc += f"`{key}`: {val.title}{('  ' + val.emoji if val.emoji else '')}\n"
            embed.title = f"{country} Not Found!"
            embed.description = desc
            embed.colour = cmn.colours.bad
            await ctx.send(embed=embed)
            return
        else:
            data = self.pfxs[country]
            embed.title = data.title + ("  " + data.emoji if data.emoji else "")
            embed.description = data.desc
            embed.colour = cmn.colours.good

            for name, val in data.calls.items():
                embed.add_field(name=name, value=val, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="contests", aliases=["cc", "tests"], category=cmn.Cats.REF)
    async def _contests(self, ctx: commands.Context):
        embed = cmn.embed_factory(ctx)
        embed.title = "Contest Calendar"
        embed.description = ("*We are currently rewriting the old, Chrome-based `contests` command. In the meantime, "
                             "use [the website](https://www.contestcalendar.com/weeklycont.php).*")
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="phoneticweight", aliases=["pw"], category=cmn.Cats.REF)
    async def _weight(self, ctx: commands.Context, *, msg: str):
        """Calculates the phonetic weight of a callsign or message."""
        embed = cmn.embed_factory(ctx)
        msg = msg.upper()
        weight = 0
        for char in msg:
            try:
                weight += self.pweights[char]
            except KeyError:
                embed.title = "Error in calculation of phonetic weight"
                embed.description = f"Unknown character `{char}` in message"
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
                return
        embed.title = f"Phonetic Weight of {msg}"
        embed.description = f"The phonetic weight is **{weight}**"
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(HamCog(bot))
