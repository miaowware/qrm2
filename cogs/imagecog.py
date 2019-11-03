"""
Image cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import io
from datetime import datetime

import discord
import discord.ext.commands as commands

import aiohttp

import global_settings as gs


class ImageCog(commands.Cog, name='Image Lookup Commands'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="plan", aliases=['bands'], category=gs.cat.ref)
    async def _bandplan(self, ctx: commands.Context, msg: str = ''):
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
                await ctx.send_help(ctx.command)
            else:
                img = discord.File(f"resources/images/bandchart/{arg}bandchart.png",
                                   filename=f'{arg}bandchart.png')
                embed = discord.Embed(title=f'{name[arg]} Amateur Radio Bands',
                                      colour=gs.colours.good,
                                      timestamp=datetime.utcnow())
                embed.set_image(url=f'attachment://{arg}bandchart.png')
                embed.set_footer(text=ctx.author.name,
                                 icon_url=str(ctx.author.avatar_url))

                await ctx.send(embed=embed, file=img)

    @commands.command(name="grayline", aliases=['greyline', 'grey', 'gray', 'gl'], category=gs.cat.maps)
    async def _grayline(self, ctx: commands.Context):
        '''Posts a map of the current greyline, where HF propagation is the best.'''
        gl_url = ('http://www.fourmilab.ch/cgi-bin/uncgi/Earth?img=NOAAtopo.evif'
                  '&imgsize=320&dynimg=y&opt=-p&lat=&lon=&alt=&tle=&date=0&utc=&jd=')
        with ctx.typing():
            embed = discord.Embed(title='Current Greyline Conditions',
                                  colour=gs.colours.good,
                                  timestamp=datetime.utcnow())
            async with aiohttp.ClientSession() as session:
                async with session.get(gl_url) as resp:
                    if resp.status != 200:
                        embed.description = 'Could not download file...'
                        embed.colour = gs.colours.bad
                    else:
                        data = io.BytesIO(await resp.read())
                        embed.set_image(url=f'attachment://greyline.jpg')
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed, file=discord.File(data, 'greyline.jpg'))

    @commands.command(name="map", category=gs.cat.maps)
    async def _map(self, ctx: commands.Context, msg: str = ''):
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
                await ctx.send_help(ctx.command)
            else:
                img = discord.File(f"resources/images/map/{arg}map.png",
                                   filename=f'{arg}map.png')
                embed = discord.Embed(title=f'{map_titles[arg]} Map',
                                      colour=gs.colours.good,
                                      timestamp=datetime.utcnow())
                embed.set_image(url=f'attachment://{arg}map.png')
                embed.set_footer(text=ctx.author.name,
                                 icon_url=str(ctx.author.avatar_url))

                await ctx.send(embed=embed, file=img)


def setup(bot: commands.Bot):
    bot.add_cog(ImageCog(bot))
