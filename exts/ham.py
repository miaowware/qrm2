"""
Ham extension for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""
import json
import random
from datetime import datetime

import discord
import discord.ext.commands as commands

import common as cmn
from resources import callsign_info


class HamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open('resources/qcodes.json') as qcode_file:
            self.qcodes = json.load(qcode_file)
        with open('resources/words') as words_file:
            self.words = words_file.read().lower().splitlines()

    @commands.command(name="qcode", aliases=['q'], category=cmn.cat.ref)
    async def _qcode_lookup(self, ctx: commands.Context, qcode: str):
        '''Look up a Q Code.'''
        with ctx.typing():
            qcode = qcode.upper()
            if qcode in self.qcodes:
                embed = discord.Embed(title=qcode, description=self.qcodes[qcode],
                                      colour=cmn.colours.good,
                                      timestamp=datetime.utcnow())
            else:
                embed = discord.Embed(title=f'Q Code {qcode} not found',
                                      colour=cmn.colours.bad,
                                      timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="phonetics", aliases=['ph', 'phoneticize', 'phoneticise', 'phone'], category=cmn.cat.fun)
    async def _phonetics_lookup(self, ctx: commands.Context, *, msg: str):
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
                                  colour=cmn.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="utc", aliases=['z'], category=cmn.cat.ref)
    async def _utc_lookup(self, ctx: commands.Context):
        '''Gets the current time in UTC.'''
        with ctx.typing():
            now = datetime.utcnow()
            result = '**' + now.strftime('%Y-%m-%d %H:%M') + 'Z**'
            embed = discord.Embed(title='The current time is:',
                                  description=result,
                                  colour=cmn.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="prefixes", aliases=["vanity", "pfx", "vanities", "prefix"])
    async def _vanity_prefixes(self, ctx: commands.Context, country: str = None):
        '''Lists valid prefixes for countries.'''
        if country is None:
            await ctx.send_help(ctx.command)
            return
        if country.lower() not in callsign_info.options:
            embed = discord.Embed(title=f'{country} not found!',
                                  description=f'Valid countries: {", ".join(callsign_info.options.keys())}',
                                  colour=cmn.colours.bad,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title=callsign_info.options[country.lower()][0],
                              description=callsign_info.options[country.lower()][1],
                              colour=cmn.colours.good,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))

        for name, val in callsign_info.options[country.lower()][2].items():
            embed.add_field(name=name, value=val, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="contests", aliases=["cc", "tests"], category=cmn.cat.ref)
    async def _contests(self, ctx: commands.Context):
        embed = discord.Embed(title="Contest Calendar",
                              timestamp=datetime.utcnow(),
                              colour=cmn.colours.good)
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))

        embed.description = ("*We are currently rewriting the old, Chrome-based `contests` command. In the meantime, "
                             "use [the website](https://www.contestcalendar.com/weeklycont.php).*")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(HamCog(bot))
