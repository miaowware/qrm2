"""
Ham cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import discord
import discord.ext.commands as commands

import json
import random
from datetime import datetime

class HamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        with open('resources/qcodes.json') as qcode_file:
            self.qcodes = json.load(qcode_file)
        self.WORDS = open('resources/words').read().lower().splitlines()

    @commands.command(name="qcode", aliases=['q'])
    async def _qcode_lookup(self, ctx, q : str):
        '''Look up a Q Code.'''
        with ctx.typing():
            q = q.upper()
            try:
                code = self.qcodes[q]
                embed = discord.Embed(title=q, description=self.qcodes[q], colour=self.gs.colours.good)
            except:
                embed = discord.Embed(title=f'Q Code {q} not found', colour=self.gs.colours.bad)
        await ctx.send(embed=embed)

    @commands.command(name="phonetics", aliases=['ph', 'phoneticize', 'phoneticise', 'phone'])
    async def _phonetics_lookup(self, ctx, *, msg : str):
        '''Get phonetics for a word or phrase.'''
        with ctx.typing():
            result = ''
            for char in msg.lower():
                if char.isalpha():
                    w = [word for word in self.WORDS if (word[0] == char)]
                    result += random.choice(w)
                else:
                    result += char
                result += ' '
            embed = discord.Embed(title=f'Phonetics for {msg}', description=result.title(), colour=self.gs.colours.good)
        await ctx.send(embed=embed)

    @commands.command(name="utc", aliases=['z'])
    async def _utc_lookup(self, ctx):
        '''Gets the current time in UTC.'''
        with ctx.typing():
            d = datetime.utcnow()
            result = '**' + d.strftime('%Y-%m-%d %H:%M') + 'Z**'
            embed = discord.Embed(title='The current time is:', description=result, colour=self.gs.colours.good)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HamCog(bot))
