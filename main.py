#!/usr/bin/env python3
"""
qrm, a bot for Discord
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


class GlobalSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.opt = opt
        self.keys = keys
        self.info = info

        self.colours = SimpleNamespace(good=0x2dc614, neutral=0x2044f7, bad=0xc91628)
        self.debug = debug_mode


# --- Bot setup ---

bot = commands.Bot(command_prefix=opt.prefix, description=info.description, help_command=commands.MinimalHelpCommand())


# --- Commands ---


# --- Events ---

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user} - {bot.user.id}")
    print("------")
    await bot.change_presence(activity=discord.Game(name="with lids on 7.200"))


# --- Run ---

bot.add_cog(GlobalSettings(bot))
bot.load_extension("cogs.infocog")

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
