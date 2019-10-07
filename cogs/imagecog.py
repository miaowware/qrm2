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

class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="plan", aliases=['bands'])
    async def _bandplan(self, ctx, msg: str = ''):
        '''Posts an image of Frequency Allocations.
    Optional argument: `cn`, `ca`, `nl`, `us`, `mx`.'''
        urls = {'cn': 'https://cdn.discordapp.com/attachments/364489754839875586/468770333223157791/Chinese_Amateur_Radio_Bands.png',
                'ca': 'https://cdn.discordapp.com/attachments/448839119934717953/469972377778782208/RAC_Bandplan_December_1_2015-1.png',
                'nl': 'http://www.pd3jdm.com/wp-content/uploads/2015/09/bandplan.jpg',
                'us': 'https://cdn.discordapp.com/attachments/377206780700393473/466729318945652737/band-chart.png',
                'mx': 'https://cdn.discordapp.com/attachments/443246106416119810/553771222421209090/mx_chart.png'}
        names = {'cn': 'Chinese',
                 'ca': 'Canadian',
                 'nl': 'Dutch',
                 'us': 'US',
                 'mx': 'Mexican'}
        arg = msg.lower()

        with ctx.typing():
            try:
                embed = discord.Embed(title=f'{names[arg]} Amateur Radio Bands', colour=self.gs.colours.good)
                embed.set_image(url=urls[arg])
            except:
                embed = discord.Embed(title=f'{names["us"]} Amateur Radio Bands', colour=self.gs.colours.good)
                embed.set_image(url=urls['us'])
        await ctx.send(embed=embed)

    @commands.command(name="cond", aliases=['condx'])
    async def _band_conditions(self, ctx, msg : str = ''):
        '''Posts an image of HF Band Conditions.'''
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get('http://www.hamqsl.com/solarsun.php') as resp:
                    if resp.status != 200:
                        return await ctx.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'condx.png'))

    @commands.command(name="grayline", aliases=['greyline', 'grey', 'gray', 'gl'])
    async def _grayline(self, ctx, msg : str = ''):
        '''Posts a map of the current greyline, where HF propagation is the best.'''
        with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get('http://www.fourmilab.ch/cgi-bin/uncgi/Earth?img=NOAAtopo.evif&imgsize=320&dynimg=y&opt=-p&lat=&lon=&alt=&tle=&date=0&utc=&jd=') as resp:
                    if resp.status != 200:
                        return await ctx.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'greyline.jpg'))

    @commands.command(name="map")
    async def _map(self, ctx, msg: str = ''):
        '''Posts an image of Frequency Allocations.
    Optional argument:`cq` = CQ Zones, `itu` = ITU Zones, `arrl` or `rac` =
    ARRL/RAC sections, `cn` = Chinese Callsign Areas, `us` = US Callsign Areas.'''
        map_urls = {"cq": 'https://cdn.discordapp.com/attachments/427925486908473344/472856720142761985/cq-zone.png',
                    "itu": 'https://cdn.discordapp.com/attachments/427925486908473344/472856796235563018/itu-zone.png',
                    "arrl": 'https://cdn.discordapp.com/attachments/427925486908473344/472856898220064778/sections.png',
                    "rac": 'https://cdn.discordapp.com/attachments/427925486908473344/472856898220064778/sections.png',
                    "cn": 'https://cdn.discordapp.com/attachments/443246106416119810/492846548242137091/2011-0802-E4B8ADE59BBDE4B89AE4BD99E58886E58CBAE59CB0E59BBEE88BB1E696871800x1344.png',
                    "us": 'https://cdn.discordapp.com/attachments/427925486908473344/472856506476265497/WASmap_Color.png'
                }
        map_titles = {"cq": 'Worldwide CQ Zones Map',
                      "itu": 'Worldwide ITU Zones Map',
                      "arrl": 'ARRL/RAC Section Map',
                      "rac":  'ARRL/RAC Section Map',
                      "cn": 'Chinese Callsign Areas',
                      "us": 'US Callsign Areas'
                  }

        arg = msg.lower()
        with ctx.typing():
            try:
                embed = discord.Embed(title=map_titles[arg], colour=self.gs.colours.good)
                embed.set_image(url=map_urls[arg])
            except:
                embed = discord.Embed(title=map_titles["us"], colour=self.gs.colours.good)
                embed.set_image(url=map_urls["us"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ImageCog(bot))
