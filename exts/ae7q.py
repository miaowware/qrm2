"""
ae7q extension for qrm
---
Copyright (C) 2019-2023 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


import discord.ext.commands as commands

from common import embed_factory, colours


class AE7QCog(commands.Cog):
    @commands.command(name="ae7q", aliases=["ae"], case_insensitive=True)
    async def _ae7q_lookup(self, ctx: commands.Context, *, _):
        """Removed in v2.8.0"""
        embed = embed_factory(ctx)
        embed.colour = colours.bad
        embed.title = "Command removed"
        embed.description = ("This command was removed in v2.8.0.\n"
                             "For context, see [this Github issue](https://github.com/miaowware/qrm2/issues/448)")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(AE7QCog())
