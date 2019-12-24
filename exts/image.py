"""
Image extension for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""

import io

import aiohttp

import discord
import discord.ext.commands as commands

import common as cmn


class ImageCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bandcharts = cmn.ImagesGroup(cmn.paths.bandcharts / "meta.json")
        self.maps = cmn.ImagesGroup(cmn.paths.maps / "meta.json")

    @commands.command(name="bandplan", aliases=['plan', 'bands'], category=cmn.cat.ref)
    async def _bandplan(self, ctx: commands.Context, region: str = ''):
        '''Posts an image of Frequency Allocations.'''
        arg = region.lower()

        with ctx.typing():
            embed = cmn.embed_factory(ctx)
            if arg not in self.bandcharts:
                desc = 'Possible arguments are:\n'
                for key, img in self.bandcharts.items():
                    desc += f'`{key}`: {img.name}{("  " + img.emoji if img.emoji else "")}\n'
                embed.title = f'Bandplan Not Found!'
                embed.description = desc
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
            else:
                metadata: cmn.ImageMetadata = self.bandcharts[arg]
                img = discord.File(cmn.paths.bandcharts / metadata.filename,
                                   filename=metadata.filename)
                if metadata.description:
                    embed.description = metadata.description
                if metadata.source:
                    embed.add_field(name="Source", value=metadata.source)
                embed.title = metadata.long_name + ("  " + metadata.emoji if metadata.emoji else "")
                embed.colour = cmn.colours.good
                embed.set_image(url='attachment://' + metadata.filename)
                await ctx.send(embed=embed, file=img)

    @commands.command(name="map", category=cmn.cat.maps)
    async def _map(self, ctx: commands.Context, map_id: str = ''):
        '''Posts an image of a ham-relevant map.'''
        arg = map_id.lower()

        with ctx.typing():
            embed = cmn.embed_factory(ctx)
            if arg not in self.maps:
                desc = 'Possible arguments are:\n'
                for key, img in self.maps.items():
                    desc += f'`{key}`: {img.name}{("  " + img.emoji if img.emoji else "")}\n'
                embed.title = 'Map Not Found!'
                embed.description = desc
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
            else:
                metadata: cmn.ImageMetadata = self.maps[arg]
                img = discord.File(cmn.paths.maps / metadata.filename,
                                   filename=metadata.filename)
                if metadata.description:
                    embed.description = metadata.description
                if metadata.source:
                    embed.add_field(name="Source", value=metadata.source)
                embed.title = metadata.long_name + ("  " + metadata.emoji if metadata.emoji else "")
                embed.colour = cmn.colours.good
                embed.set_image(url='attachment://' + metadata.filename)
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


def setup(bot: commands.Bot):
    bot.add_cog(ImageCog(bot))
