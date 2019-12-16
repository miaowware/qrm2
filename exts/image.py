"""
Image extension for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""

import io
from datetime import datetime

import discord
import discord.ext.commands as commands

import aiohttp

import common as cmn


class ImageCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="bandplan", aliases=['plan', 'bands'], category=cmn.cat.ref)
    async def _bandplan(self, ctx: commands.Context, region: str = ''):
        '''Posts an image of Frequency Allocations.'''
        name = {'cn': 'Chinese',
                'ca': 'Canadian',
                'nl': 'Dutch',
                'us': 'US',
                'mx': 'Mexican'}
        arg = region.lower()

        with ctx.typing():
            embed = cmn.embed_factory(ctx)
            if arg not in name:
                desc = 'Possible arguments are:\n'
                for abbrev, title in name.items():
                    desc += f'`{abbrev}`: {title}\n'
                embed.title = f'Bandplan Not Found!'
                embed.description = desc
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
            else:
                img = discord.File(f"resources/images/bandchart/{arg}bandchart.png",
                                   filename=f'{arg}bandchart.png')
                embed.title = f'{name[arg]} Amateur Radio Bands'
                embed.colour = cmn.colours.good
                embed.set_image(url=f'attachment://{arg}bandchart.png')
                await ctx.send(embed=embed, file=img)

    @commands.command(name="grayline", aliases=['greyline', 'grey', 'gray', 'gl'], category=cmn.cat.maps)
    async def _grayline(self, ctx: commands.Context):
        '''Posts a map of the current greyline, where HF propagation is the best.'''
        gl_url = ('http://www.fourmilab.ch/cgi-bin/uncgi/Earth?img=NOAAtopo.evif'
                  '&imgsize=320&dynimg=y&opt=-p&lat=&lon=&alt=&tle=&date=0&utc=&jd=')
        with ctx.typing():
            embed = cmn.embed_factory(ctx)
            embed.title = 'Current Greyline Conditions'
            embed.colour = cmn.colours.good
            async with aiohttp.ClientSession() as session:
                async with session.get(gl_url) as resp:
                    if resp.status != 200:
                        embed.description = 'Could not download file...'
                        embed.colour = cmn.colours.bad
                    else:
                        data = io.BytesIO(await resp.read())
                        embed.set_image(url=f'attachment://greyline.jpg')
        await ctx.send(embed=embed, file=discord.File(data, 'greyline.jpg'))

    @commands.command(name="map", category=cmn.cat.maps)
    async def _map(self, ctx: commands.Context, map_id: str = ''):
        '''Posts an image of a ham-relevant map.'''
        map_titles = {"cq": 'Worldwide CQ Zones Map',
                      "itu": 'Worldwide ITU Zones Map',
                      "arrl": 'ARRL/RAC Section Map',
                      "rac":  'ARRL/RAC Section Map',
                      "cn": 'Chinese Callsign Areas',
                      "us": 'US Callsign Areas'}

        arg = map_id.lower()
        with ctx.typing():
            embed = cmn.embed_factory(ctx)
            if arg not in map_titles:
                desc = 'Possible arguments are:\n'
                for abbrev, title in map_titles.items():
                    desc += f'`{abbrev}`: {title}\n'
                embed.title = 'Map Not Found!'
                embed.description = desc
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
            else:
                img = discord.File(f"resources/images/map/{arg}map.png",
                                   filename=f'{arg}map.png')
                embed.title = f'{map_titles[arg]}'
                embed.colour = cmn.colours.good
                embed.set_image(url=f'attachment://{arg}map.png')
                await ctx.send(embed=embed, file=img)


def setup(bot: commands.Bot):
    bot.add_cog(ImageCog(bot))
