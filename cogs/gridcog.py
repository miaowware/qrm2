"""
Grid cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import math
from datetime import datetime

import discord
import discord.ext.commands as commands

import common as cmn


class GridCog(commands.Cog, name='Location Commands'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="grid", category=cmn.cat.maps)
    async def _grid_sq_lookup(self, ctx: commands.Context, lat: str, lon: str):
        '''Calculates the grid square for latitude and longitude coordinates,
with negative being latitude South and longitude West.'''
        with ctx.typing():
            grid = "**"
            try:
                latf = float(lat) + 90
                lonf = float(lon) + 180
                if 0 <= latf <= 180 and 0 <= lonf <= 360:
                    grid += chr(ord('A') + int(lonf / 20))
                    grid += chr(ord('A') + int(latf / 10))
                    grid += chr(ord('0') + int((lonf % 20)/2))
                    grid += chr(ord('0') + int((latf % 10)/1))
                    grid += chr(ord('a') + int((lonf - (int(lonf/2)*2)) / (5/60)))
                    grid += chr(ord('a') + int((latf - (int(latf/1)*1)) / (2.5/60)))
                    grid += "**"
                    embed = discord.Embed(title=f'Maidenhead Grid Locator for {float(lat):.6f}, {float(lon):.6f}',
                                          description=grid,
                                          colour=cmn.colours.good,
                                          timestamp=datetime.utcnow())
                    embed.set_footer(text=ctx.author.name,
                                     icon_url=str(ctx.author.avatar_url))
                else:
                    raise ValueError('Out of range.')
            except ValueError as err:
                msg = f'Error generating grid square for {lat}, {lon}.'
                embed = discord.Embed(title=msg, description=str(err),
                                      colour=cmn.colours.bad,
                                      timestamp=datetime.utcnow())
                embed.set_footer(text=ctx.author.name,
                                 icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="ungrid", aliases=['loc'], category=cmn.cat.maps)
    async def _location_lookup(self, ctx: commands.Context, grid: str, grid2: str = None):
        '''Calculates the latitude and longitude for the center of a grid square.
If two grid squares are given, the distance and azimuth between them is calculated.'''
        with ctx.typing():
            if grid2 is None or grid2 == '':
                try:
                    grid = grid.upper()
                    loc = get_coords(grid)

                    if len(grid) >= 6:
                        embed = discord.Embed(title=f'Latitude and Longitude for {grid}',
                                              description=f'**{loc[0]:.5f}, {loc[1]:.5f}**',
                                              colour=cmn.colours.good,
                                              url=f'https://www.openstreetmap.org/#map=13/{loc[0]:.5f}/{loc[1]:.5f}',
                                              timestamp=datetime.utcnow())

                    else:
                        embed = discord.Embed(title=f'Latitude and Longitude for {grid}',
                                              description=f'**{loc[0]:.1f}, {loc[1]:.1f}**',
                                              colour=cmn.colours.good,
                                              url=f'https://www.openstreetmap.org/#map=10/{loc[0]:.1f}/{loc[1]:.1f}',
                                              timestamp=datetime.utcnow())
                    embed.set_footer(text=ctx.author.name,
                                     icon_url=str(ctx.author.avatar_url))
                except Exception as e:
                    msg = f'Error generating latitude and longitude for grid {grid}.'
                    embed = discord.Embed(title=msg, description=str(e),
                                          colour=cmn.colours.bad,
                                          timestamp=datetime.utcnow())
                    embed.set_footer(text=ctx.author.name,
                                     icon_url=str(ctx.author.avatar_url))
            else:
                radius = 6371
                try:
                    grid = grid.upper()
                    grid2 = grid2.upper()
                    loc = get_coords(grid)
                    loc2 = get_coords(grid2)
                    # Haversine formula
                    d_lat = math.radians(loc2[0] - loc[0])
                    d_lon = math.radians(loc2[1] - loc[1])
                    a = math.sin(d_lat/2) ** 2 +\
                        math.cos(math.radians(loc[0])) * math.cos(math.radians(loc2[0])) *\
                        math.sin(d_lon/2) ** 2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                    d = radius * c
                    d_mi = 0.6213712 * d

                    # Bearing
                    y_dist = math.sin(math.radians(loc2[1]-loc[1])) * math.cos(math.radians(loc2[0]))
                    x_dist = math.cos(math.radians(loc[0])) * math.sin(math.radians(loc2[0])) -\
                        math.sin(math.radians(loc[0])) * math.cos(math.radians(loc2[0])) *\
                        math.cos(math.radians(loc2[1] - loc[1]))
                    bearing = (math.degrees(math.atan2(y_dist, x_dist)) + 360) % 360

                    des = f'**Distance:** {d:.1f} km ({d_mi:.1f} mi)\n**Bearing:** {bearing:.1f}°'
                    embed = discord.Embed(title=f'Great Circle Distance and Bearing from {grid} to {grid2}',
                                          description=des,
                                          colour=cmn.colours.good,
                                          timestamp=datetime.utcnow())
                    embed.set_footer(text=ctx.author.name,
                                     icon_url=str(ctx.author.avatar_url))
                except Exception as e:
                    msg = f'Error generating great circle distance and bearing from {grid} and {grid2}.'
                    embed = discord.Embed(title=msg, description=str(e),
                                          colour=cmn.colours.bad,
                                          timestamp=datetime.utcnow())
                    embed.set_footer(text=ctx.author.name,
                                     icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)


def get_coords(grid: str):
    if len(grid) < 3:
        raise ValueError('The grid locator must be at least 4 characters long.')

    if not grid[0:2].isalpha() or not grid[2:4].isdigit():
        if len(grid) <= 4:
            raise ValueError('The grid locator must be of the form AA##.')
        if len(grid) >= 6 and not grid[5:7].isalpha():
            raise ValueError('The grid locator must be of the form AA##AA.')

    lon = ((ord(grid[0]) - ord('A')) * 20) - 180
    lat = ((ord(grid[1]) - ord('A')) * 10) - 90
    lon += ((ord(grid[2]) - ord('0')) * 2)
    lat += ((ord(grid[3]) - ord('0')) * 1)

    if len(grid) >= 6:
        # have subsquares
        lon += ((ord(grid[4])) - ord('A')) * (5/60)
        lat += ((ord(grid[5])) - ord('A')) * (2.5/60)
        # move to center of subsquare
        lon += (2.5/60)
        lat += (1.25/60)
        return (lat, lon)
    # move to center of square
    lon += 1
    lat += 0.5
    return (lat, lon)


def setup(bot: commands.Bot):
    bot.add_cog(GridCog(bot))
