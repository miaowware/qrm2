"""
Common tools for the bot.
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
---

`colours`: Colours used by embeds.

`cat`: Category names for the HelpCommand.
"""


import traceback
from datetime import datetime
from types import SimpleNamespace
from typing import Union

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


def embed_factory(ctx: commands.Context, title: str, desc: str,
                  colour: Union[discord.Colour, int] = colours.neutral, url: str = "") -> discord.Embed:
    """Creates an embed"""
    embed = discord.Embed(title=title,
                          description=desc,
                          timestamp=datetime.utcnow(),
                          colour=colour,
                          url=url)
    embed.set_footer(text=ctx.author,
                     icon_url=str(ctx.author.avatar_url))
    return embed


def error_embed_factory(ctx: commands.Context, exception: Exception, debug_mode: bool) -> discord.Embed:
    """Creates an Error embed."""
    if debug_mode:
        fmtd_ex = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    else:
        fmtd_ex = traceback.format_exception_only(exception.__class__, exception)
    desc = "```\n" + '\n'.join(fmtd_ex) + "```"
    return embed_factory(ctx, "Error", desc, colours.bad)


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
