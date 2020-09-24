#!/usr/bin/env python3
"""
qrm, a bot for Discord
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import asyncio
import random
import sys
import traceback
from datetime import datetime, time
from types import SimpleNamespace

import pytz

import discord
from discord.ext import commands, tasks

import info
import common as cmn
import utils.connector as conn

import data.keys as keys
import data.options as opt


# --- Settings ---

exit_code = 1  # The default exit code. ?shutdown and ?restart will change it accordingly (fail-safe)

ext_dir = "exts"  # The name of the directory where extensions are located.

debug_mode = opt.debug  # Separate assignement in-case we define an override (ternary operator goes here)


# --- Bot setup ---

# Loop/aiohttp stuff
loop = asyncio.get_event_loop()
connector = loop.run_until_complete(conn.new_connector())

bot = commands.Bot(command_prefix=opt.prefix,
                   case_insensitive=True,
                   description=info.description, help_command=commands.MinimalHelpCommand(),
                   loop=loop,
                   connector=connector)

# Simple way to access bot-wide stuff in extensions.
bot.qrm = SimpleNamespace()

# Let's store stuff here.
bot.qrm.connector = connector
bot.qrm.debug_mode = debug_mode


# --- Commands ---

@bot.command(name="restart", aliases=["rs"], category=cmn.cat.admin)
@commands.check(cmn.check_if_owner)
async def _restart_bot(ctx: commands.Context):
    """Restarts the bot."""
    global exit_code
    await cmn.add_react(ctx.message, cmn.emojis.check_mark)
    print(f"[**] Restarting! Requested by {ctx.author}.")
    exit_code = 42  # Signals to the wrapper script that the bot needs to be restarted.
    await bot.logout()


@bot.command(name="shutdown", aliases=["shut"], category=cmn.cat.admin)
@commands.check(cmn.check_if_owner)
async def _shutdown_bot(ctx: commands.Context):
    """Shuts down the bot."""
    global exit_code
    await cmn.add_react(ctx.message, cmn.emojis.check_mark)
    print(f"[**] Shutting down! Requested by {ctx.author}.")
    exit_code = 0  # Signals to the wrapper script that the bot should not be restarted.
    await bot.logout()


@bot.group(name="extctl", aliases=["ex"], case_insensitive=True, category=cmn.cat.admin)
@commands.check(cmn.check_if_owner)
async def _extctl(ctx: commands.Context):
    """Extension control commands.
    Defaults to `list` if no subcommand specified"""
    if ctx.invoked_subcommand is None:
        cmd = bot.get_command("extctl list")
        await ctx.invoke(cmd)


@_extctl.command(name="list", aliases=["ls"])
async def _extctl_list(ctx: commands.Context):
    """Lists loaded extensions."""
    embed = cmn.embed_factory(ctx)
    embed.title = "Loaded Extensions"
    embed.description = "\n".join(["‣ " + x.split(".")[1] for x in bot.extensions.keys()])
    await ctx.send(embed=embed)


@_extctl.command(name="load", aliases=["ld"])
async def _extctl_load(ctx: commands.Context, extension: str):
    """Loads an extension."""
    bot.load_extension(ext_dir + "." + extension)
    await cmn.add_react(ctx.message, cmn.emojis.check_mark)


@_extctl.command(name="reload", aliases=["rl", "r", "relaod"])
async def _extctl_reload(ctx: commands.Context, extension: str):
    """Reloads an extension."""
    if ctx.invoked_with == "relaod":
        pika = bot.get_emoji(opt.pika)
        if pika:
            await cmn.add_react(ctx.message, pika)
    bot.reload_extension(ext_dir + "." + extension)
    await cmn.add_react(ctx.message, cmn.emojis.check_mark)


@_extctl.command(name="unload", aliases=["ul"])
async def _extctl_unload(ctx: commands.Context, extension: str):
    """Unloads an extension."""
    bot.unload_extension(ext_dir + "." + extension)
    await cmn.add_react(ctx.message, cmn.emojis.check_mark)


# --- Events ---

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user} - {bot.user.id}")
    print("------")
    if opt.status_mode == "time":
        _ensure_activity_time.start()
    elif opt.status_mode == "random":
        _ensure_activity_random.start()
    else:
        _ensure_activity_fixed.start()


@bot.event
async def on_message(message):
    msg = message.content.lower()
    for emoji, keywords in opt.msg_reacts.items():
        if any([keyword in msg for keyword in keywords]):
            await message.add_reaction(discord.utils.find(lambda x: x.id == emoji, bot.emojis))

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError):
    if isinstance(err, commands.UserInputError):
        await cmn.add_react(ctx.message, cmn.emojis.warning)
        await ctx.send_help(ctx.command)
    elif isinstance(err, commands.CommandNotFound):
        if ctx.invoked_with.startswith(("?", "!")):
            return
        else:
            await cmn.add_react(ctx.message, cmn.emojis.question)
    elif isinstance(err, commands.CheckFailure):
        # Add handling of other subclasses of CheckFailure as needed.
        if isinstance(err, commands.NotOwner):
            await cmn.add_react(ctx.message, cmn.emojis.no_entry)
        else:
            await cmn.add_react(ctx.message, cmn.emojis.x)
    elif isinstance(err, commands.DisabledCommand):
        await cmn.add_react(ctx.message, cmn.emojis.bangbang)
    elif isinstance(err, (commands.CommandInvokeError, commands.ConversionError)):
        # Emulating discord.py's default beaviour.
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)

        embed = cmn.error_embed_factory(ctx, err.original, bot.qrm.debug_mode)
        embed.description += f"\n`{type(err).__name__}`"
        await cmn.add_react(ctx.message, cmn.emojis.warning)
        await ctx.send(embed=embed)
    else:
        # Emulating discord.py's default beaviour. (safest bet)
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)
        await cmn.add_react(ctx.message, cmn.emojis.warning)


# --- Tasks ---

@tasks.loop(minutes=5)
async def _ensure_activity_time():
    status = opt.statuses[0]

    try:
        tz = pytz.timezone(opt.status_tz)
    except pytz.exceptions.UnknownTimeZoneError:
        status = "with invalid timezones"
        if opt.show_help:
            status += f" | {opt.display_prefix}help"
        await bot.change_presence(activity=discord.Game(name=status))
        return

    now = datetime.now(tz=tz).time()

    for sts in opt.time_statuses:
        start_time = time(hour=sts[1][0], minute=sts[1][1], tzinfo=tz)
        end_time = time(hour=sts[2][0], minute=sts[2][1], tzinfo=tz)
        if start_time < now <= end_time:
            status = sts[0]
            if opt.show_help:
                status += f" | {opt.display_prefix}help"

    await bot.change_presence(activity=discord.Game(name=status))


@tasks.loop(minutes=5)
async def _ensure_activity_random():
    status = random.choice(opt.statuses)
    if opt.show_help:
        status += f" | {opt.display_prefix}help"

    await bot.change_presence(activity=discord.Game(name=status))


@tasks.loop(minutes=5)
async def _ensure_activity_fixed():
    status = opt.statuses[0]
    if opt.show_help:
        status += f" | {opt.display_prefix}help"

    await bot.change_presence(activity=discord.Game(name=status))


# --- Run ---

for ext in opt.exts:
    bot.load_extension(ext_dir + "." + ext)


try:
    bot.run(keys.discord_token)

except discord.LoginFailure as ex:
    # Miscellaneous authentications errors: borked token and co
    if bot.qrm.debug_mode:
        raise
    raise SystemExit("Error: Failed to authenticate: {}".format(ex))

except discord.ConnectionClosed as ex:
    # When the connection to the gateway (websocket) is closed
    if bot.qrm.debug_mode:
        raise
    raise SystemExit("Error: Discord gateway connection closed: [Code {}] {}".format(ex.code, ex.reason))

except ConnectionResetError as ex:
    # More generic connection reset error
    if bot.qrm.debug_mode:
        raise
    raise SystemExit("ConnectionResetError: {}".format(ex))


# --- Exit ---
# Codes for the wrapper shell script:
# 0 - Clean exit, don't restart
# 1 - Error exit, [restarting is up to the shell script]
# 42 - Clean exit, do restart

raise SystemExit(exit_code)
