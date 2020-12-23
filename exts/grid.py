"""
Grid extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import gridtools

import discord.ext.commands as commands

import common as cmn


class GridCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="grid", category=cmn.cat.maps)
    async def _grid_sq_lookup(self, ctx: commands.Context, lat: float, lon: float):
        ("""Calculates the grid square for latitude and longitude coordinates."""
         """\n\nCoordinates should be in decimal format, with negative being latitude South and longitude West."""
         """\n\nTo calculate the latitude and longitude from a grid locator, use `latlong`""")
        latlong = gridtools.LatLong(lat, lon)
        grid = gridtools.Grid(latlong)

        embed = cmn.embed_factory(ctx)
        embed.title = f"Maidenhead Grid Locator for {latlong.lat:.5f}, {latlong.long:.5f}"
        embed.description = f"**{grid}**"
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="latlong", aliases=["latlon", "loc", "ungrid"], category=cmn.cat.maps)
    async def _location_lookup(self, ctx: commands.Context, grid: str):
        ("""Calculates the latitude and longitude for the center of a grid locator."""
         """\n\nTo calculate the grid locator from a latitude and longitude, use `grid`"""
         """\n\n*Warning: `ungrid` will be removed soon. Use one of the other names for this command.*""")
        grid_obj = gridtools.Grid(grid)

        embed = cmn.embed_factory(ctx)
        embed.title = f"Latitude and Longitude for {grid_obj}"
        embed.colour = cmn.colours.good
        embed.description = f"**{grid_obj.lat:.5f}, {grid_obj.long:.5f}**"
        if ctx.invoked_with == "ungrid":
            embed.add_field(name="Warning", value=(f"*`{ctx.prefix}ungrid` will be removed soon, use `{ctx.prefix}help "
                                                   "latlong` to see other names for this command.*"))
        await ctx.send(embed=embed)

    @commands.command(name="griddistance", aliases=["griddist", "distance", "dist"], category=cmn.cat.maps)
    async def _dist_lookup(self, ctx: commands.Context, grid1: str, grid2: str):
        """Calculates the great circle distance and azimuthal bearing between two grid locators."""
        g1 = gridtools.Grid(grid1)
        g2 = gridtools.Grid(grid2)

        dist, bearing = gridtools.grid_distance(g1, g2)
        dist_mi = 0.6214 * dist

        embed = cmn.embed_factory(ctx)
        embed.title = f"Great Circle Distance and Bearing from {g1} to {g2}"
        embed.description = f"**Distance:** {dist:.1f} km ({dist_mi:.1f} mi)\n**Bearing:** {bearing:.1f}°"
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(GridCog(bot))
