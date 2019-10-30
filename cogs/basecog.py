"""
Base cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

from datetime import datetime
import re
from collections import OrderedDict

import discord
import discord.ext.commands as commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="info", aliases=["about"])
    async def _info(self, ctx):
        """Shows info about qrm."""
        embed = discord.Embed(title="About qrm",
                              description=self.gs.info.description,
                              colour=self.gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        embed = embed.add_field(name="Authors", value=", ".join(self.gs.info.authors))
        embed = embed.add_field(name="Contributing", value=self.gs.info.contributing)
        embed = embed.add_field(name="License", value=self.gs.info.license)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def _ping(self, ctx: commands.Context):
        """Show the current latency to the discord endpoint."""
        embed = discord.Embed(title="**Pong!**",
                              description=f'Current ping is {self.bot.latency*1000:.1f} ms',
                              colour=self.gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="changelog", aliases=["clog"])
    async def _changelog(self, ctx: commands.Context):
        """Show what has changed in recent bot versions."""
        embed = discord.Embed(title="qrm Changelog",
                              description="For a full listing, visit [Github](https://github.com/classabbyamp/discord-qrm-bot/blob/master/CHANGELOG.md).",
                              colour=self.gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        changelog = await parse_changelog()

        vers = 0
        for ver, log in changelog.items():
            if ver.lower() != 'unreleased':
                if 'date' in log:
                    header = f'**{ver}** ({log["date"]})'
                else:
                    header = f'**{ver}**'
                embed.add_field(name=header, value=await format_changelog(log), inline=False)
                vers += 1
            if vers >= 2:
                break

        await ctx.send(embed=embed)


async def parse_changelog():
    changelog = OrderedDict()
    ver = ''
    heading = ''

    with open('CHANGELOG.md') as changelog_file:
        for line in changelog_file.readlines():
            if line.strip() == '':
                continue
            if re.match(r'##[^#]', line):
                ver_match = re.match(r'\[(.+)\](?: - )?(\d{4}-\d{2}-\d{2})?', line.lstrip('#').strip())
                ver = ver_match.group(1)
                changelog[ver] = dict()
                if ver_match.group(2):
                    changelog[ver]['date'] = ver_match.group(2)
            elif re.match(r'###[^#]', line):
                heading = line.lstrip('#').strip()
                changelog[ver][heading] = []
            elif ver != '' and heading != '':
                changelog[ver][heading].append(line.lstrip('-').strip())
    return changelog


async def format_changelog(log: dict):
    formatted = ''
    for header, lines in log.items():
        if header != 'date':
            formatted += f'**{header}**\n'
            for line in lines:
                formatted += f'- {line}\n'
    return formatted


def setup(bot: commands.Bot):
    bot.add_cog(BaseCog(bot))
