"""
Fun extension for qrm
---
Copyright (C) 2019-2023 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


import json
import random

import discord.ext.commands as commands

import common as cmn

import data.options as opt


class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open(cmn.paths.resources / "imgs.1.json") as file:
            self.imgs: dict = json.load(file)
        with open(cmn.paths.resources / "words.1.txt") as words_file:
            self.words = words_file.read().lower().splitlines()

    @commands.command(name="xkcd", aliases=["x"], category=cmn.Cats.FUN)
    async def _xkcd(self, ctx: commands.Context, number: int):
        """Looks up an xkcd comic by number."""
        await ctx.send("http://xkcd.com/" + str(number))

    @commands.command(name="tar", category=cmn.Cats.FUN)
    async def _tar(self, ctx: commands.Context):
        """Returns xkcd: tar."""
        await ctx.send("http://xkcd.com/1168")

    @commands.command(name="standards", category=cmn.Cats.FUN)
    async def _standards(self, ctx: commands.Context):
        """Returns xkcd: Standards."""
        await ctx.send("http://xkcd.com/927")

    @commands.command(name="worksplit", aliases=["split", "ft8"], category=cmn.Cats.FUN)
    async def _worksplit(self, ctx: commands.Context):
        """Posts "Work split you lids"."""
        embed = cmn.embed_factory(ctx)
        embed.title = "Work Split, You Lids!"
        embed.set_image(url=opt.resources_url + self.imgs["worksplit"])
        await ctx.send(embed=embed)

    @commands.command(name="xd", hidden=True, category=cmn.Cats.FUN)
    async def _xd(self, ctx: commands.Context):
        """ecks dee"""
        await ctx.send("ECKS DEE :smirk:")

    @commands.command(name="funetics", aliases=["fun"], category=cmn.Cats.FUN)
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

    @commands.command(name="uwuify", aliases=["uwu"], category=cmn.Cats.FUN)
    async def _uwuify(self, ctx: commands.Context, *, msg: str):
        """UwUify your text"""
        trans_table = msg.maketrans({"l": "w", "L": "W", "r": "w", "R": "W"})
        uwuified_text = msg.replace('na', 'nya').translate(trans_table).replace("no", "yo").replace("mo", "yo")
        await ctx.send(uwuified_text)


def setup(bot: commands.Bot):
    bot.add_cog(FunCog(bot))
