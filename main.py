#!/usr/bin/env python3
"""
qrm, a bot for Discord
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""

import discord
from discord.ext import commands, tasks

import common as cmn
import info

import data.options as opt
import data.keys as keys


# --- Settings ---

exit_code = 1  # The default exit code. ?shutdown and ?restart will change it accordingly (fail-safe)

ext_dir = "exts"  # The name of the directory where extensions are located.

debug_mode = opt.debug  # Separate assignement in-case we define an override (ternary operator goes here)


# --- Bot setup ---

bot = commands.Bot(command_prefix=opt.prefix,
                   description=info.description,
                   help_command=commands.MinimalHelpCommand())


# --- Commands ---

@bot.command(name="restart", hidden=True)
@commands.check(cmn.check_if_owner)
async def _restart_bot(ctx: commands.Context):
    """Restarts the bot."""
    global exit_code
    await cmn.add_react(ctx.message, cmn.emojis.good)
    print(f"[**] Restarting! Requested by {ctx.author}.")
    exit_code = 42  # Signals to the wrapper script that the bot needs to be restarted.
    await bot.logout()


@bot.command(name="shutdown", hidden=True)
@commands.check(cmn.check_if_owner)
async def _shutdown_bot(ctx: commands.Context):
    """Shuts down the bot."""
    global exit_code
    await cmn.add_react(ctx.message, cmn.emojis.good)
    print(f"[**] Shutting down! Requested by {ctx.author}.")
    exit_code = 0  # Signals to the wrapper script that the bot should not be restarted.
    await bot.logout()


@bot.group(name="extctl", hidden=True)
@commands.check(cmn.check_if_owner)
async def _extctl(ctx: commands.Context):
    """Extension control commands.
    Defaults to `list` if no subcommand specified"""
    if ctx.invoked_subcommand is None:
        cmd = bot.get_command("extctl list")
        await ctx.invoke(cmd)


@_extctl.command(name="list")
async def _extctl_list(ctx: commands.Context):
    """Lists Extensions."""
    embed = cmn.embed_factory(ctx)
    embed.title = "Loaded Extensions"
    embed.description = "\n".join(["‣ " + x.split(".")[1] for x in bot.extensions.keys()])
    await ctx.send(embed=embed)


@_extctl.command(name="load")
async def _extctl_load(ctx: commands.Context, extension: str):
    try:
        bot.load_extension(ext_dir + "." + extension)
        await cmn.add_react(ctx.message, cmn.emojis.good)
    except commands.ExtensionError as ex:
        embed = cmn.error_embed_factory(ctx, ex, debug_mode)
        await ctx.send(embed=embed)


@_extctl.command(name="reload")
async def _extctl_reload(ctx: commands.Context, extension: str):
    try:
        bot.reload_extension(ext_dir + "." + extension)
        await cmn.add_react(ctx.message, cmn.emojis.good)
    except commands.ExtensionError as ex:
        embed = cmn.error_embed_factory(ctx, ex, debug_mode)
        await ctx.send(embed=embed)


@_extctl.command(name="unload")
async def _extctl_unload(ctx: commands.Context, extension: str):
    try:
        bot.unload_extension(ext_dir + "." + extension)
        await cmn.add_react(ctx.message, cmn.emojis.good)
    except commands.ExtensionError as ex:
        embed = cmn.error_embed_factory(ctx, ex, debug_mode)
        await ctx.send(embed=embed)


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

for ext in opt.exts:
    bot.load_extension(ext_dir + '.' + ext)

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
