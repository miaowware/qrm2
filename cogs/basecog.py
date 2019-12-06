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

import info

import options as opt
import common as gs


class QrmHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={'help': 'Shows help about qrm or a command',
                                        'aliases': ['h']})

    def get_bot_mapping(self):
        bot = self.context.bot
        mapping = {}
        for cmd in bot.commands:
            cat = cmd.__original_kwargs__.get('category', None)
            if cat in mapping:
                mapping[cat].append(cmd)
            else:
                mapping[cat] = [cmd]
        return mapping

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if command.aliases != []:
            aliases = ', '.join(command.aliases)
            fmt = command.name
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
            return f'{opt.prefix}{alias} {command.signature}\n    *Aliases:* {aliases}'
        alias = command.name if not parent else f'{parent} {command.name}'
        return f'{opt.prefix}{alias} {command.signature}'

    async def send_error_message(self, error):
        embed = discord.Embed(title='qrm Help Error',
                              description=error,
                              colour=gs.colours.bad,
                              timestamp=datetime.utcnow()
                              )
        embed.set_footer(text=self.context.author.name,
                         icon_url=str(self.context.author.avatar_url))
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='qrm Help',
                              description=f'For command-specific help and usage, use `{opt.prefix}help [command name]`',
                              colour=gs.colours.neutral,
                              timestamp=datetime.utcnow()
                              )
        embed.set_footer(text=self.context.author.name,
                         icon_url=str(self.context.author.avatar_url))

        for cat, cmds in mapping.items():
            cmds = list(filter(lambda x: not x.hidden, cmds))
            if cmds == []:
                continue
            names = sorted([cmd.name for cmd in cmds])
            if cat is not None:
                embed.add_field(name=cat.title(), value=', '.join(names), inline=False)
            else:
                embed.add_field(name='Other', value=', '.join(names), inline=False)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command),
                              description=command.help,
                              colour=gs.colours.neutral,
                              timestamp=datetime.utcnow()
                              )
        embed.set_footer(text=self.context.author.name,
                         icon_url=str(self.context.author.avatar_url))
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=self.get_command_signature(group),
                              description=group.help,
                              colour=gs.colours.neutral,
                              timestamp=datetime.utcnow()
                              )
        embed.set_footer(text=self.context.author.name,
                         icon_url=str(self.context.author.avatar_url))
        for cmd in group.commands:
            embed.add_field(name=self.get_command_signature(cmd), value=cmd.help, inline=False)
        await self.context.send(embed=embed)


class BaseCog(commands.Cog, name='Basic Commands'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = QrmHelpCommand()
        bot.help_command.cog = self
        self.changelog = parse_changelog()

    @commands.command(name="info", aliases=["about"])
    async def _info(self, ctx: commands.Context):
        """Shows info about qrm."""
        embed = discord.Embed(title="About qrm",
                              description=info.description,
                              colour=gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        embed = embed.add_field(name="Authors", value=", ".join(info.authors))
        embed = embed.add_field(name="Contributing", value=info.contributing)
        embed = embed.add_field(name="License", value=info.license)
        embed = embed.add_field(name="Version", value=f'v{info.release} (Released: {info.release_timestamp})')
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def _ping(self, ctx: commands.Context):
        """Show the current latency to the discord endpoint."""
        embed = discord.Embed(title="**Pong!**",
                              description=f'Current ping is {self.bot.latency*1000:.1f} ms',
                              colour=gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(name="changelog", aliases=["clog"])
    async def _changelog(self, ctx: commands.Context):
        """Show what has changed in recent bot versions."""
        embed = discord.Embed(title="qrm Changelog",
                              description=("For a full listing, visit [Github](https://"
                                           "github.com/classabbyamp/discord-qrm-bot/blob/master/CHANGELOG.md)."),
                              colour=self.gs.colours.neutral,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        changelog = self.changelog

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

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def parse_changelog():
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
