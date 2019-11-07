"""
Morse Code cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import json
from datetime import datetime

import discord
import discord.ext.commands as commands

import global_settings as gs


class MorseCog(commands.Cog, name='Morse Code Commands'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open('resources/morse.json') as morse_file:
            self.ascii2morse = json.load(morse_file)
            self.morse2ascii = {v: k for k, v in self.ascii2morse.items()}

    @commands.command(name="morse", aliases=['cw'], category=gs.cat.ref)
    async def _morse(self, ctx: commands.Context, *, msg: str):
        """Converts ASCII to international morse code."""
        with ctx.typing():
            result = ''
            for char in msg.upper():
                try:
                    result += self.ascii2morse[char]
                except KeyError:
                    result += '<?>'
                result += ' '
            embed = discord.Embed(title=f'Morse Code for {msg}',
                                  description=result,
                                  colour=gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="unmorse", aliases=['demorse', 'uncw', 'decw'], category=gs.cat.ref)
    async def _unmorse(self, ctx: commands.Context, *, msg: str):
        '''Converts international morse code to ASCII.'''
        with ctx.typing():
            result = ''
            msg0 = msg
            msg = msg.split('/')
            msg = [m.split() for m in msg]
            for word in msg:
                for char in word:
                    try:
                        result += self.morse2ascii[char]
                    except KeyError:
                        result += '<?>'
                result += ' '
            embed = discord.Embed(title=f'ASCII for {msg0}',
                                  description=result,
                                  colour=gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="weight", aliases=["cwweight", 'cww'], category=gs.cat.ref)
    async def _weight(self, ctx: commands.Context, *, msg: str):
        '''Calculates the CW Weight of a callsign or message.'''
        with ctx.typing():
            msg = msg.upper()
            weight = 0
            for char in msg:
                try:
                    cw_char = self.ascii2morse[char].replace('-', '==')
                    weight += len(cw_char) * 2 + 2
                except KeyError:
                    res = f'Unknown character {char} in callsign'
                    await ctx.send(res)
                    return
            res = f'The CW weight is **{weight}**'
            embed = discord.Embed(title=f'CW Weight of {msg}',
                                  description=res,
                                  colour=gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(MorseCog(bot))
