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


# --- Settings ---

exit_code = 1  # The default exit code. ?shutdown and ?restart will change it accordingly (fail-safe)

debug_mode = opt.debug  # Separate assignement in-case we define an override (ternary operator goes here)


class GlobalSettings(commands.Cog):
    def __init__(self, bot: commands.Bot):
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


# --- Helper functions ---

async def add_react(msg: discord.Message, react: str):
    '''Adds a react to a message.'''
    try:
        await msg.add_reaction(react)
    except discord.Forbidden:
        print(f"!! Missing permissions to add reaction in '{msg.guild.id}/{msg.channel.id}'!")


# --- Checks ---

async def check_if_owner(ctx: commands.Context):
    '''Checks if the user running the command is a bot owner.'''
    if ctx.author.id in opt.owners_uids:
        return True
    await add_react(ctx.message, "❌")
    return False


# --- Commands ---

@bot.command(name="restart")
@commands.check(check_if_owner)
async def _restart_bot(ctx: commands.Context):
    """Restarts the bot."""
    global exit_code
    await add_react(ctx.message, "✅")
    exit_code = 42  # Signals to the wrapper script that the bot needs to be restarted.
    await bot.logout()


@bot.command(name="shutdown")
@commands.check(check_if_owner)
async def _shutdown_bot(ctx: commands.Context):
    """Shuts down the bot."""
    global exit_code
    await add_react(ctx.message, "✅")
    exit_code = 0  # Signals to the wrapper script that the bot should not be restarted.
    await bot.logout()


# --- Events ---

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user} - {bot.user.id}")
    print("------")


# --- Tasks ---

@tasks.loop(minutes=5)
async def _ensure_activity():
    await bot.change_presence(activity=discord.Game(name=opt.game))


@_ensure_activity.before_loop
async def _before_ensure_activity():
    await bot.wait_until_ready()


# --- Run ---

bot.add_cog(GlobalSettings(bot))
for cog in opt.cogs:
    bot.load_extension(f"cogs.{cog}")

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
    raise SystemExit("Error: Discord gateway connection closed: [Code {}] {}".format(ex.code, ex.reason))

except ConnectionResetError as ex:
    # More generic connection reset error
    if debug_mode:
        raise
    raise SystemExit("ConnectionResetError: {}".format(ex))

# --- Exit ---
# Codes for the wrapper shell script:
# 0 - Clean exit, don't restart
# 1 - Error exit, [restarting is up to the shell script]
# 42 - Clean exit, do restart

raise SystemExit(exit_code)
