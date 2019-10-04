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


bot = commands.Bot(command_prefix=opt.prefix, description=info.description)


bot.run(keys.discord_token)
