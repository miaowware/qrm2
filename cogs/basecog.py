"""
Base cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

from datetime import datetime

import discord
import discord.ext.commands as commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="info", aliases=["about"])
    async def _info(self, ctx):
        """Shows info about qrm."""
        embed = discord.Embed(title="About qrm",
                              description=self.gs.info.description,
                              colour=self.gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        embed = embed.add_field(name="Authors", value=", ".join(self.gs.info.authors))
        embed = embed.add_field(name="Contributing", value=self.gs.info.contributing)
        embed = embed.add_field(name="License", value=self.gs.info.license)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def _ping(self, ctx: commands.Context):
        """Show the current latency to the discord endpoint."""
        embed = discord.Embed(title="**Pong!**",
                              description=f'Current ping is {self.bot.latency*1000:.1f} ms',
                              colour=self.gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(BaseCog(bot))
