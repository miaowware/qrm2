#!/usr/bin/env python3
"""
Qrm, a bot for Discord
---

[copyright here]
"""

from types import SimpleNamespace

import discord
import discord.ext.commands as commands

import info

import options as opt
import keys


# --- Global settings ---

debug_mode = opt.debug  # Separate assignement in-case we define an override (ternary operator goes here)


bot_colours = SimpleNamespace(good=0x2dc614, neutral=0x2044f7, bad=0xc91628)


# --- Bot setup ---

bot = commands.Bot(command_prefix=opt.prefix, description=info.description, help_command=commands.MinimalHelpCommand())


# --- Commands ---

@bot.command(name="info", aliases=["about"])
async def _info(ctx):
    """Shows info about qrm."""
    embed = discord.Embed(title="About qrm", description=info.description, colour=bot_colours.neutral)
    embed = embed.add_field(name="Authors", value=", ".join(info.authors))
    embed = embed.add_field(name="Contributing", value=info.contributing)
    embed = embed.add_field(name="License", value=info.license)
    await ctx.send(embed=embed)

try:
    bot.run(keys.discord_token)

except discord.LoginFailure as ex:  # Miscellaneous authentications errors: borked token and co
    if debug_mode:
        raise
    raise SystemExit("Error: Failed to authenticate: {}".format(ex))

except discord.ConnectionClosed as ex:  # When the connection the the gateway (websocket) is closed
    if debug_mode:
        raise
    raise SystemExit("Error: Discord gateway connection closed: [Code {}] {}".format(ex.code, ex.reason))

except ConnectionResetError as ex:  # More generic connection reset error
    if debug_mode:
        raise
    raise SystemExit("ConnectionResetError: {}".format(ex))
