#!/usr/bin/env python3
"""
qrm, a bot for Discord
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

from types import SimpleNamespace

import discord
from discord.ext import commands, tasks

import info

import options as opt
import keys


# --- Global settings ---

debug_mode = opt.debug  # Separate assignement in-case we define an override (ternary operator goes here)


class GlobalSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.opt = opt
        self.keys = keys
        self.info = info

        self.colours = SimpleNamespace(good=0x43B581,
                                       neutral=0x7289DA,
                                       bad=0xF04747)
        self.debug = debug_mode


# --- Bot setup ---

bot = commands.Bot(command_prefix=opt.prefix,
                   description=info.description,
                   help_command=commands.MinimalHelpCommand())

# --- Commands ---


# --- Events ---

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user} - {bot.user.id}")
    print("------")


# --- Tasks ---

@tasks.loop(minutes=5)
async def _ensure_activity():
    await bot.change_presence(activity=discord.Game(name="with lids on 7.200"))


@_ensure_activity.before_loop
async def _before_ensure_activity():
    await bot.wait_until_ready()


# --- Run ---

bot.add_cog(GlobalSettings(bot))
bot.load_extension("cogs.basecog")
bot.load_extension("cogs.morsecog")
bot.load_extension("cogs.funcog")
bot.load_extension("cogs.imagecog")
bot.load_extension("cogs.studycog")

_ensure_activity.start()


try:
    bot.run(keys.discord_token)

except discord.LoginFailure as ex:
    # Miscellaneous authentications errors: borked token and co
    if debug_mode:
        raise
    raise SystemExit("Error: Failed to authenticate: {}".format(ex))

except discord.ConnectionClosed as ex:
    # When the connection to the gateway (websocket) is closed
    if debug_mode:
        raise
    raise SystemExit( "Error: Discord gateway connection closed: [Code {}] {}" .format(ex.code, ex.reason))

except ConnectionResetError as ex:
    # More generic connection reset error
    if debug_mode:
        raise
    raise SystemExit("ConnectionResetError: {}".format(ex))

