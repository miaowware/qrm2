"""
Lookup cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import discord
from discord.ext import commands, tasks

import json
from datetime import datetime
from util import cty_json


class LookupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        self.CTY = None
        self.CTY_list = None
        self.up_cty_first_run = True

    @commands.command(name="ae7q", aliases=['ae'])
    async def _ae7q_lookup(self, ctx, c: str):
        '''Links to info about a callsign from AE7Q.'''
        await ctx.send(f'http://ae7q.com/query/data/CallHistory.php?CALL={c}')

    @commands.command(name="qrz")
    async def _qrz_lookup(self, ctx, call: str):
        '''Links to info about a callsign from QRZ.'''
        await ctx.send(f'http://qrz.com/db/{call}')

    @commands.command(name="sat")
    async def _sat_lookup(self, ctx, sat: str, grid1: str, grid2: str = None):
        '''Links to info about satellite passes on satmatch.com.
    Usage: `?sat sat_name grid1 grid2`'''
        now = datetime.utcnow().strftime('%Y-%m-%d%%20%H:%M')
        if grid2 is None or grid2 == '':
            await ctx.send(
                      f'http://www.satmatch.com/satellite/{sat}/obs1/{grid1}' +
                      f'?search_start_time={now}&duration_hrs=24'
                  )
        else:
            await ctx.send(
                      f'http://www.satmatch.com/satellite/{sat}/obs1/{grid1}' +
                      f'/obs2/{grid2}?search_start_time={now}&duration_hrs=24'
                  )

    @commands.command(name="dxcc", aliases=['dx'])
    async def _dxcc_lookup(self, ctx, q: str):
        '''Gets info about a prefix.'''
        with ctx.typing():
            noMatch = True
            qMatch = None
            q = q.upper()
            q0 = q
            if q != 'LAST_UPDATED':
                embed = discord.Embed(title=f'DXCC Info for {q0}')
                embed.description = f'Prefix {q0} not found'
                embed.colour = self.gs.colours.bad
                while noMatch:
                    if q in self.CTY_list:
                        qMatch = q
                        noMatch = False
                    else:
                        q = q[:-1]
                        if len(q) == 0:
                            noMatch = False
                    if qMatch is not None:
                        d = self.CTY[qMatch]
                        embed = embed.add_field(name="Entity",
                                                value=d['entity'])
                        embed = embed.add_field(name="CQ Zone",
                                                value=d['cq'])
                        embed = embed.add_field(name="ITU Zone",
                                                value=d['itu'])
                        embed = embed.add_field(name="Continent",
                                                value=d['continent'])
                        tz = d['tz']
                        if tz > 0:
                            tz = '+' + str(tz)
                        embed = embed.add_field(name="Time Zone", value=tz)
                        embed.description = ''
                        embed.colour = self.gs.colours.good
            else:
                updatedDate = self.CTY['last_updated'][0:4] + '-'
                updatedDate += self.CTY['last_updated'][4:6] + '-'
                updatedDate += self.CTY['last_updated'][6:8]
                r = f'CTY.DAT last updated on {updatedDate}'
                embed = discord.Embed(title=r, colour=self.gs.colours.neutral)
        await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def _update_cty(self):
        print('Checking for CTY update...')
        regen = cty_json.genCtyJson()
        if regen or self.up_cty_first_run:
            with open('resources/cty.json') as ctyfile:
                print('Reloading CTY JSON data...')
                self.CTY = json.load(ctyfile)
                self.CTY_list = list(self.CTY.keys())
                self.CTY_list.sort()
                self.CTY_list.sort(key=len, reverse=True)
            self.up_cty_first_run = False


def setup(bot):
    lookupcog = LookupCog(bot)
    bot.add_cog(lookupcog)
    lookupcog._update_cty.start()
