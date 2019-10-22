"""
Base cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

from datetime import datetime
import itertools

import discord
import discord.ext.commands as commands


class QrmHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={'help': 'Shows help about qrm or a command',
                                        'aliases': ['h']})

    def get_command_signature(self, command):
        gs = self.context.bot.get_cog("GlobalSettings")
        parent = command.full_parent_name
        if command.aliases != []:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{gs.opt.prefix}{alias} {command.signature}'

    async def send_error_message(self, error):
        gs = self.context.bot.get_cog("GlobalSettings")
        embed = discord.Embed(title='qrm Help Error',
                              description=error,
                              colour=gs.colours.bad,
                              timestamp=datetime.utcnow()
                              )
        embed.set_footer(text=self.context.author.name,
                         icon_url=str(self.context.author.avatar_url))
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping):
        gs = self.context.bot.get_cog("GlobalSettings")
        embed = discord.Embed(title='qrm Help',
                              description=f'For command-specific help and usage, use `{gs.opt.prefix}help [command name]`',
                              colour=gs.colours.neutral,
                              timestamp=datetime.utcnow()
                              )
        embed.set_footer(text=self.context.author.name,
                         icon_url=str(self.context.author.avatar_url))

        for cog, cmds in mapping.items():
            cmds = list(filter(lambda x: not x.hidden, cmds))
            if cmds == []:
                continue
            names = [cmd.name for cmd in cmds]
            if cog is not None:
                embed.add_field(name=cog.qualified_name, value=', '.join(names), inline=False)
            else:
                embed.add_field(name='Other Commands', value=', '.join(names), inline=False)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        gs = self.context.bot.get_cog("GlobalSettings")
        embed = discord.Embed(title=self.get_command_signature(command),
                              description=command.help,
                              colour=gs.colours.neutral,
                              timestamp=datetime.utcnow()
                              )
        embed.set_footer(text=self.context.author.name,
                         icon_url=str(self.context.author.avatar_url))
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        gs = self.context.bot.get_cog("GlobalSettings")
        embed = discord.Embed(title=f'{group.name} Help',
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
        self.gs = bot.get_cog("GlobalSettings")
        self._original_help_command = bot.help_command
        bot.help_command = QrmHelpCommand()
        bot.help_command.cog = self

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
        embed = embed.add_field(name="Version", value=f'{self.gs.info.release} (Released: {self.gs.info.release_timestamp})')
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

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot: commands.Bot):
    bot.add_cog(BaseCog(bot))
