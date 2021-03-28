"""
Contest Calendar extension for qrm
---
Copyright (C) 2021 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import discord.ext.commands as commands

import common as cmn


class ContestCalendarCog(commands.Cog):
    @commands.command(name="contests", aliases=["cc", "tests"], category=cmn.Cats.LOOKUP)
    async def _contests(self, ctx: commands.Context):
        embed = cmn.embed_factory(ctx)
        embed.title = "Contest Calendar"
        embed.description = ("*We are currently rewriting the old, Chrome-based `contests` command. In the meantime, "
                             "use [the website](https://www.contestcalendar.com/weeklycont.php).*")
        embed.colour = cmn.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ContestCalendarCog(bot))
