"""
Fun cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import discord.ext.commands as commands


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="xkcd", aliases=['x'])
    async def _xkcd(self, ctx, num: str):
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
