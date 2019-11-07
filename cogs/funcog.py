"""
Fun cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import discord.ext.commands as commands

import global_settings as gs


class FunCog(commands.Cog, name='Fun Commands'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="xkcd", aliases=['x'], category=gs.cat.fun)
    async def _xkcd(self, ctx: commands.Context, number: str):
        '''Look up an xkcd by number.'''
        await ctx.send('http://xkcd.com/' + number)

    @commands.command(name="tar", category=gs.cat.fun)
    async def _tar(self, ctx: commands.Context):
        '''Returns an xkcd about tar.'''
        await ctx.send('http://xkcd.com/1168')

    @commands.command(name="xd", hidden=True, category=gs.cat.fun)
    async def _xd(self, ctx: commands.Context):
        '''ecks dee'''
        await ctx.send('ECKS DEE :smirk:')


def setup(bot: commands.Bot):
    bot.add_cog(FunCog(bot))
