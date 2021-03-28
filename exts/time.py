"""
Time extension for qrm
---
Copyright (C) 2021 classabbyamp, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


from datetime import datetime

import discord.ext.commands as commands

import common as cmn


class TimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="utc", aliases=["z"], category=cmn.Cats.TIME)
    async def _utc_lookup(self, ctx: commands.Context):
        """Returns the current time in UTC."""
        now = datetime.utcnow()
        result = "**" + now.strftime("%Y-%m-%d %H:%M") + "Z**"
        embed = cmn.embed_factory(ctx)
        embed.title = "The current time is:"
        embed.description = result
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(TimeCog(bot))
