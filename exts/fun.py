"""
Fun extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import random

import discord.ext.commands as commands

import common as cmn


class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("resources/words") as words_file:
            self.words = words_file.read().lower().splitlines()

    @commands.command(name="xkcd", aliases=["x"], category=cmn.cat.fun)
    async def _xkcd(self, ctx: commands.Context, number: str):
        """Looks up an xkcd comic by number."""
        await ctx.send("http://xkcd.com/" + number)

    @commands.command(name="tar", category=cmn.cat.fun)
    async def _tar(self, ctx: commands.Context):
        """Returns xkcd: tar."""
        await ctx.send("http://xkcd.com/1168")

    @commands.command(name="standards", category=cmn.cat.fun)
    async def _standards(self, ctx: commands.Context):
        """Returns xkcd: Standards."""
        await ctx.send("http://xkcd.com/927")

    @commands.command(name="xd", hidden=True, category=cmn.cat.fun)
    async def _xd(self, ctx: commands.Context):
        """ecks dee"""
        await ctx.send("ECKS DEE :smirk:")

    @commands.command(name="funetics", aliases=["fun"], category=cmn.cat.fun)
    async def _funetics_lookup(self, ctx: commands.Context, *, msg: str):
        """Generates fun/wacky phonetics for a word or phrase."""
        result = ""
        for char in msg.lower():
            if char.isalpha():
                result += random.choice([word for word in self.words if word[0] == char])
            else:
                result += char
            result += " "
        embed = cmn.embed_factory(ctx)
        embed.title = f"Funetics for {msg}"
        embed.description = result.title()
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(FunCog(bot))
