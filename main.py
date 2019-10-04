#!/usr/bin/env python3
"""
Qrm, a bot for Discord
---

[copyright here]
"""

import discord
import discord.ext.commands as commands

import info

import options as opt
import keys

# --- Variables ---
debug_mode = opt.debug

bot = commands.Bot(command_prefix=opt.prefix, description=info.description)


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
