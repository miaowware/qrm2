"""
Codes extension for qrm
---
Copyright (C) 2019-2021 classabbyamp, 0x5c  (as ham.py)
Copyright (C) 2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


import json

import discord.ext.commands as commands

import common as cmn


class HamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open(cmn.paths.resources / "phonetics.1.json") as file:
            d = json.load(file)
            self.phonetics: dict[str, str] = d["phonetics"]
            self.pweights: dict[str, int] = d["pweights"]
        with open(cmn.paths.resources / "qcodes.1.json") as file:
            self.qcodes: dict = json.load(file)

    @commands.command(name="qcode", aliases=["q"], category=cmn.Cats.CODES)
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

    @commands.command(name="phonetics", aliases=["ph", "phoneticize", "phoneticise", "phone"], category=cmn.Cats.CODES)
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

    @commands.command(name="phoneticweight", aliases=["pw"], category=cmn.Cats.CODES)
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
