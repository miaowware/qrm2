"""
Lookup cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

from datetime import datetime
import threading

import discord
from discord.ext import commands, tasks

from ctyparser import BigCty


class LookupCog(commands.Cog):
    def __init__(self, bot: commmands.Bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        try:
            self.CTY = BigCty('./data/cty.json')
        except OSError:
            self.CTY = BigCty()
            update = threading.Thread(target=run_update, args=(self.CTY, "./data/cty.json"))
            update.start()

    @commands.command(name="sat")
    async def _sat_lookup(self, ctx: commands.Context, sat: str, grid1: str, grid2: str = None):
        '''Links to info about satellite passes on satmatch.com.
    Usage: `?sat sat_name grid1 grid2`'''
        now = datetime.utcnow().strftime('%Y-%m-%d%%20%H:%M')
        if grid2 is None or grid2 == '':
            await ctx.send(f'http://www.satmatch.com/satellite/{sat}/obs1/{grid1}'
                           f'?search_start_time={now}&duration_hrs=24')
        else:
            await ctx.send(f'http://www.satmatch.com/satellite/{sat}/obs1/{grid1}'
                           f'/obs2/{grid2}?search_start_time={now}&duration_hrs=24')

    @commands.command(name="dxcc", aliases=['dx'])
    async def _dxcc_lookup(self, ctx: commands.Context, query: str):
        '''Gets info about a prefix.'''
        with ctx.typing():
            noMatch = True
            queryMatch = None
            query = query.upper()
            if query != 'LAST_UPDATED':
                embed = discord.Embed(title=f'DXCC Info for {query}',
                                      timestamp=datetime.utcnow())
                embed.set_footer(text=f'{ctx.author.name} | Last Updated: {self.CTY.formatted_version}',
                                 icon_url=str(ctx.author.avatar_url))
                embed.description = f'Prefix {query} not found'
                embed.colour = self.gs.colours.bad
                while noMatch:
                    if query in self.CTY.keys():
                        queryMatch = query
                        noMatch = False
                    else:
                        query = query[:-1]
                        if len(query) == 0:
                            noMatch = False
                    if queryMatch is not None:
                        data = self.CTY[queryMatch]
                        embed = embed.add_field(name="Entity",
                                                value=data['entity'])\
                                     .add_field(name="CQ Zone",
                                                value=data['cq'])\
                                     .add_field(name="ITU Zone",
                                                value=data['itu'])\
                                     .add_field(name="Continent",
                                                value=data['continent'])\
                                     .add_field(name="Time Zone",
                                                value=f'+{data["tz"]}' if data['tz'] > 0 else str(data['tz']))
                        embed.description = ''
                        embed.colour = self.gs.colours.good
            else:
                result = f'CTY.DAT last updated on {self.CTY.formatted_version}'
                embed = discord.Embed(title=result, colour=self.gs.colours.neutral)
                embed.set_footer(text=f'{ctx.author.name}',
                                 icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def _update_cty(self):
        update = threading.Thread(target=run_update, args=(self.CTY, "./data/cty.json"))
        update.start()

    def cog_unload(self):
        self.CTY.dump("./data/cty.json")


def run_update(cty_obj, dump_loc):
    update = cty_obj.update()
    if update:
        cty_obj.dump(dump_loc)


def setup(bot: commands.Bot):
    lookupcog = LookupCog(bot)
    bot.add_cog(lookupcog)
    lookupcog._update_cty.start()
