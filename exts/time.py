"""
Time extension for qrm
---
Copyright (C) 2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


from datetime import datetime, timedelta

import discord.ext.commands as commands

import common as cmn


class TimeCog(commands.Cog):
    offsets = [
            ("Y", "", timedelta(hours=-12)),
            ("X", "", timedelta(hours=-11)),
            ("W", "", timedelta(hours=-10)),
            ("V", "", timedelta(hours=-9)),
            ("U", "", timedelta(hours=-8)),
            ("T", "", timedelta(hours=-7)),
            ("S", "", timedelta(hours=-6)),
            ("R", "", timedelta(hours=-5)),
            ("Q", "", timedelta(hours=-4)),
            ("P", "", timedelta(hours=-3)),
            ("O", "", timedelta(hours=-2)),
            ("N", "", timedelta(hours=-1)),
            ("Z", "UTC", timedelta(hours=0)),
            ("A", "", timedelta(hours=+1)),
            ("B", "", timedelta(hours=+2)),
            ("C", "", timedelta(hours=+3)),
            ("D", "", timedelta(hours=+4)),
            ("E", "", timedelta(hours=+5)),
            ("F", "", timedelta(hours=+6)),
            ("G", "", timedelta(hours=+7)),
            ("H", "", timedelta(hours=+8)),
            ("I", "", timedelta(hours=+9)),
            ("K", "", timedelta(hours=+10)),
            ("L", "", timedelta(hours=+11)),
            ("M", "", timedelta(hours=+12))
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="utc", aliases=["z"], category=cmn.Cats.TIME)
    async def _utc_lookup(self, ctx: commands.Context):
        """Returns the current time in UTC."""
        now = datetime.utcnow()
        result = "**" + now.strftime("%Y-%m-%d %H:%M") + "Z**"
        embed = cmn.embed_factory(ctx)
        embed.title = "The current time is:"
        embed.description = result
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="miltime", category=cmn.Cats.TIME)
    async def miltime(self, ctx: commands.Context):
        """Prints the current time in all 25 military time zones."""
        time = ctx.message.created_at
        embed = cmn.embed_factory(ctx)
        embed.title = f"{cmn.emojis.clock} Military Time Zones Now"
        embed.colour = cmn.colours.good
        embed.description = "```"
        embed.description += "\n".join([f"{x}: {time + z :%Y-%m-%d %H:%M} {y}" for x, y, z in self.offsets])
        embed.description += "```"
        embed.add_field(name="Notes", value=(
            "**J** is not present in the table, and is used for local time.\n"
            "The zones are referenced by their letters, using phonetics.\n"
            f"You can check the NATO phonetics for a letter using the `{ctx.prefix}phonetics` command."
            ))
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(TimeCog(bot))
