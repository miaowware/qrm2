"""
Ham cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""
import json
import random
from datetime import datetime

import discord
import discord.ext.commands as commands


class HamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        with open('resources/qcodes.json') as qcode_file:
            self.qcodes = json.load(qcode_file)
        with open('resources/words') as words_file:
            self.words = words_file.read().lower().splitlines()

    @commands.command(name="qcode", aliases=['q'])
    async def _qcode_lookup(self, ctx, qcode: str):
        '''Look up a Q Code.'''
        with ctx.typing():
            qcode = qcode.upper()
            if qcode in self.qcodes:
                embed = discord.Embed(title=qcode, description=self.qcodes[qcode],
                                      colour=self.gs.colours.good,
                                      timestamp=datetime.utcnow())
            else:
                embed = discord.Embed(title=f'Q Code {qcode} not found',
                                      colour=self.gs.colours.bad,
                                      timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="phonetics", aliases=['ph', 'phoneticize', 'phoneticise', 'phone'])
    async def _phonetics_lookup(self, ctx, *, msg: str):
        '''Get phonetics for a word or phrase.'''
        with ctx.typing():
            result = ''
            for char in msg.lower():
                if char.isalpha():
                    result += random.choice([word for word in self.words if word[0] == char])
                else:
                    result += char
                result += ' '
            embed = discord.Embed(title=f'Phonetics for {msg}',
                                  description=result.title(),
                                  colour=self.gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="utc", aliases=['z'])
    async def _utc_lookup(self, ctx):
        '''Gets the current time in UTC.'''
        with ctx.typing():
            now = datetime.utcnow()
            result = '**' + now.strftime('%Y-%m-%d %H:%M') + 'Z**'
            embed = discord.Embed(title='The current time is:',
                                  description=result,
                                  colour=self.gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HamCog(bot))
