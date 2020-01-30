"""
Ham extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""

from datetime import datetime

import discord.ext.commands as commands

import common as cmn
from resources import callsign_info
from resources import phonetics
from resources import qcodes


class HamCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="qcode", aliases=['q'], category=cmn.cat.ref)
    async def _qcode_lookup(self, ctx: commands.Context, qcode: str):
        '''Look up a Q Code.'''
        with ctx.typing():
            qcode = qcode.upper()
            embed = cmn.embed_factory(ctx)
            if qcode in qcodes.qcodes:
                embed.title = qcode
                embed.description = qcodes.qcodes[qcode]
                embed.colour = cmn.colours.good
            else:
                embed.title = f'Q Code {qcode} not found'
                embed.colour = cmn.colours.bad
        await ctx.send(embed=embed)

    @commands.command(name="phonetics", aliases=['ph', 'phoneticize', 'phoneticise', 'phone'], category=cmn.cat.ref)
    async def _phonetics_lookup(self, ctx: commands.Context, *, msg: str):
        '''Get phonetics for a word or phrase.'''
        with ctx.typing():
            result = ''
            for char in msg.lower():
                if char.isalpha():
                    result += phonetics.phonetics[char]
                else:
                    result += char
                result += ' '
            embed = cmn.embed_factory(ctx)
            embed.title = f'Phonetics for {msg}'
            embed.description = result.title()
            embed.colour = cmn.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="utc", aliases=['z'], category=cmn.cat.ref)
    async def _utc_lookup(self, ctx: commands.Context):
        '''Gets the current time in UTC.'''
        with ctx.typing():
            now = datetime.utcnow()
            result = '**' + now.strftime('%Y-%m-%d %H:%M') + 'Z**'
            embed = cmn.embed_factory(ctx)
            embed.title = 'The current time is:'
            embed.description = result
            embed.colour = cmn.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="prefixes", aliases=["vanity", "pfx", "vanities", "prefix"], category=cmn.cat.ref)
    async def _vanity_prefixes(self, ctx: commands.Context, country: str = None):
        '''Lists valid prefixes for countries.'''
        if country is None:
            await ctx.send_help(ctx.command)
            return
        embed = cmn.embed_factory(ctx)
        if country.lower() not in callsign_info.options:
            embed.title = f'{country} not found!'
            embed.description = f'Valid countries: {", ".join(callsign_info.options.keys())}'
            embed.colour = cmn.colours.bad
        else:
            embed.title = callsign_info.options[country.lower()][0]
            embed.description = callsign_info.options[country.lower()][1]
            embed.colour = cmn.colours.good

            for name, val in callsign_info.options[country.lower()][2].items():
                embed.add_field(name=name, value=val, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="contests", aliases=["cc", "tests"], category=cmn.cat.ref)
    async def _contests(self, ctx: commands.Context):
        embed = cmn.embed_factory(ctx)
        embed.title = "Contest Calendar"
        embed.description = ("*We are currently rewriting the old, Chrome-based `contests` command. In the meantime, "
                             "use [the website](https://www.contestcalendar.com/weeklycont.php).*")
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(HamCog(bot))
