"""
Image cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import discord
import discord.ext.commands as commands

import aiohttp
import io
from datetime import datetime


class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="plan", aliases=['bands'])
    async def _bandplan(self, ctx, msg: str = ''):
        '''Posts an image of Frequency Allocations.
    Optional argument: `cn`, `ca`, `nl`, `us`, `mx`.'''
        name = {'cn': 'Chinese',
                'ca': 'Canadian',
                'nl': 'Dutch',
                'us': 'US',
                'mx': 'Mexican'}
        arg = msg.lower()

        with ctx.typing():
            if arg not in name:
                arg = 'us'
            img = discord.File(f"resources/images/{arg}bandchart.png",
                               filename=f'{arg}bandchart.png')
            embed = discord.Embed(title=f'{name[arg]} Amateur Radio Bands',
                                  colour=self.gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_image(url=f'attachment://{arg}bandchart.png')
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))

        await ctx.send(embed=embed, file=img)

    @commands.command(name="cond", aliases=['condx'])
    async def _band_conditions(self, ctx, msg: str = ''):
        '''Posts an image of HF Band Conditions.'''
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get('http://www.hamqsl.com/solarsun.php') as resp:
                    if resp.status != 200:
                        return await ctx.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
            embed = discord.Embed(title='Current Solar Conditions',
                                  colour=self.gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_image(url=f'attachment://condx.png')
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed, file=discord.File(data, 'condx.png'))

    @commands.command(name="grayline", aliases=['greyline', 'grey', 'gray', 'gl'])
    async def _grayline(self, ctx, msg: str = ''):
        '''Posts a map of the current greyline, where HF propagation is the best.'''
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get('http://www.fourmilab.ch/cgi-bin/uncgi/Earth?img=NOAAtopo.evif&imgsize=320&dynimg=y&opt=-p&lat=&lon=&alt=&tle=&date=0&utc=&jd=') as resp:
                    if resp.status != 200:
                        return await ctx.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
            embed = discord.Embed(title='Current Greyline Conditions',
                                  colour=self.gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_image(url=f'attachment://greyline.jpg')
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed, file=discord.File(data, 'greyline.jpg'))

    @commands.command(name="map")
    async def _map(self, ctx, msg: str = ''):
        '''Posts an image of Frequency Allocations.
    Optional argument:`cq` = CQ Zones, `itu` = ITU Zones, `arrl` or `rac` =
    ARRL/RAC sections, `cn` = Chinese Callsign Areas, `us` = US Callsign Areas.'''
        map_titles = {"cq": 'Worldwide CQ Zones Map',
                      "itu": 'Worldwide ITU Zones Map',
                      "arrl": 'ARRL/RAC Section Map',
                      "rac":  'ARRL/RAC Section Map',
                      "cn": 'Chinese Callsign Areas',
                      "us": 'US Callsign Areas'}

        arg = msg.lower()
        with ctx.typing():
            if arg not in map_titles:
                arg = 'us'
            img = discord.File(f"resources/images/{arg}map.png",
                               filename=f'{arg}map.png')
            embed = discord.Embed(title=f'{map_titles[arg]} Map',
                                  colour=self.gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_image(url=f'attachment://{arg}map.png')
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))

        await ctx.send(embed=embed, file=img)


def setup(bot):
    bot.add_cog(ImageCog(bot))
