"""
Base cog for qrm
---

Copyright (C) 2019  Abigail Gold, 0x5c

This file is part of discord-qrmbot.

discord-qrmbot is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import discord
import discord.ext.commands as commands


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="info", aliases=["about"])
    async def _info(self, ctx):
        """Shows info about qrm."""
        embed = discord.Embed(title="About qrm", description=self.gs.info.description, colour=self.gs.colours.neutral)
        embed = embed.add_field(name="Authors", value=", ".join(self.gs.info.authors))
        embed = embed.add_field(name="Contributing", value=self.gs.info.contributing)
        embed = embed.add_field(name="License", value=self.gs.info.license)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def _ping(self, ctx):
        await ctx.send(f'**Pong!** Current ping is {self.bot.latency*1000:.1f} ms')


def setup(bot):
    bot.add_cog(BaseCog(bot))
