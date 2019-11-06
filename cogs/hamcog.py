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
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        with open('resources/qcodes.json') as qcode_file:
            self.qcodes = json.load(qcode_file)
        with open('resources/words') as words_file:
            self.words = words_file.read().lower().splitlines()

    @commands.command(name="qcode", aliases=['q'])
    async def _qcode_lookup(self, ctx: commands.Context, qcode: str):
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
                                  colour=self.gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="utc", aliases=['z'])
    async def _utc_lookup(self, ctx: commands.Context):
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

    @commands.command(name="vanities", aliases=["vanity", "pfx", "prefixes", "prefix"])
    async def _vanity_prefixes(self, ctx: commands.Context):
        '''Lists valid vanity prefixes for the US.'''
        embed = discord.Embed(title='Valid US Vanity Prefixes',
                              description=('#x# is the number of letters in the prefix and suffix of a callsign.'
                                           'E.g., WY4RC would be a 2x2 callsign, with prefix WY and suffix RC.'),
                              colour=self.gs.colours.good,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))

        group_a = ('**Any:** K, N, W (1x2)\n'
                   '    AA-AL, KA-KZ, NA-NZ, WA-WZ (2x1)\n'
                   '    AA-AL (2x2)\n'
                   '*Except*\n'
                   '**Alaska:** AL, KL, NL, WL (2x1)\n'
                   '**Caribbean:** KP, NP, WP (2x1)\n'
                   '**Pacific:** AH, KH, NH, WH (2x1)')

        embed.add_field(name='**Group A** (Extra Only)', value=group_a, inline=False)

        group_b = ('**Any:** K, N, W (1x2)\n'
                   '    AA-AL, KA-KZ, NA-NZ, WA-WZ (2x1)\n'
                   '    AA-AL (2x2)\n'
                   '*Except*\n'
                   '**Alaska:** AL, KL, NL, WL (2x1)\n'
                   '**Caribbean:** KP, NP, WP (2x1)\n'
                   '**Pacific:** AH, KH, NH, WH (2x1)')

        embed.add_field(name='**Group B** (Advanced and Extra Only)', value=group_b, inline=False)

        group_c = ('**Any Region:** K, N, W (1x3)\n'
                   '*Except*\n'
                   '**Alaska:** KL, NL, WL (2x2)\n'
                   '**Caribbean:** NP, WP (2x2)\n'
                   '**Pacific:** KH, NH, WH (2x2)')

        embed.add_field(name='**Group C** (Technician, General, Advanced, Extra Only)', value=group_c, inline=False)

        group_d = ('**Any Region:** KA-KZ, WA-WZ (2x3)\n'
                   '*Except*\n'
                   '**Alaska:** KL, WL (2x3)\n'
                   '**Caribbean:** KP, WP (2x3)\n'
                   '**Pacific:** KH, WH (2x3)')

        embed.add_field(name='**Group D** (Any License Class)', value=group_d, inline=False)

        unavail = ('- KA2AA-KA9ZZ, KC4AAA-KC4AAF, KC4USA-KC4USZ, KG4AA-KG4ZZ, KC6AA-KC6ZZ, KL9KAA-KL9KHZ, KX6AA-KX6ZZ\n'
                   '- Any suffix SOS or QRA-QUZ\n'
                   '- Any 2x3 with X as the first suffix letter\n'
                   '- Any 2x3 with AF, KF, NF, or WF prefix and suffix EMA\n'
                   '- Any 2x3 with AA-AL, NA-NZ, WC, WK, WM, WR, or WT prefix\n'
                   '- Any 2x1, 2x2, or 2x3 with KP, NP, WP prefix and 0, 6, 7, 8, 9 numeral\n'
                   '- Any 1x1 callsign')

        embed.add_field(name='**Unavailable**', value=unavail, inline=False)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(HamCog(bot))
