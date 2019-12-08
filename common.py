"""
Common tools for the bot.
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
---

`colours`: Colours used by embeds.

`cat`: Category names for the HelpCommand.
"""


import traceback
from datetime import datetime
from types import SimpleNamespace

import discord
import discord.ext.commands as commands


import data.options as opt


__all__ = ["colours", "cat", "emojis", "error_embed_factory", "add_react", "check_if_owner"]


# --- Common values ---

colours = SimpleNamespace(good=0x43B581,
                          neutral=0x7289DA,
                          bad=0xF04747)
# meow
cat = SimpleNamespace(lookup='Information Lookup',
                      fun='Fun',
                      maps='Mapping',
                      ref='Reference',
                      study='Exam Study',
                      weather='Land and Space Weather')

emojis = SimpleNamespace(good='✅',
                         bad='❌')


# --- Helper functions ---

def error_embed_factory(ctx: commands.Context, exception: Exception, debug_mode: bool) -> discord.Embed:
    """Creates an Error embed."""
    if debug_mode:
        fmtd_ex = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    else:
        fmtd_ex = traceback.format_exception_only(exception.__class__, exception)
    embed = discord.Embed(title="Error",
                          timestamp=datetime.utcnow(),
                          colour=colours.bad)
    embed.set_footer(text=ctx.author,
                     icon_url=str(ctx.author.avatar_url))
    embed.description = "```\n" + '\n'.join(fmtd_ex) + "```"
    return embed


async def add_react(msg: discord.Message, react: str):
    try:
        await msg.add_reaction(react)
    except discord.Forbidden:
        print(f"[!!] Missing permissions to add reaction in '{msg.guild.id}/{msg.channel.id}'!")


# --- Checks ---

async def check_if_owner(ctx: commands.Context):
    if ctx.author.id in opt.owners_uids:
        return True
    await add_react(ctx.message, emojis.bad)
    return False
