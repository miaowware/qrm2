"""
Fun cog for qrm
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


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="xkcd", aliases=['x'])
    async def _xkcd(self, ctx, num : str):
        '''Look up an xkcd by number.'''
        await ctx.send('http://xkcd.com/' + num)

    @commands.command(name="tar")
    async def _tar(self, ctx):
        '''Returns an xkcd about tar.'''
        await ctx.send('http://xkcd.com/1168')

    @commands.command(name="xd")
    async def _xd(self, ctx):
        '''ecks dee'''
        await ctx.send('ECKS DEE :smirk:')


def setup(bot):
    bot.add_cog(FunCog(bot))
