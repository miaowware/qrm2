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


import collections
import json
import traceback
from pathlib import Path
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

paths = SimpleNamespace(data=Path("./data/"),
                        resources=Path("./resources/"),
                        bandcharts=Path("./resources/img/bandcharts/"),
                        maps=Path("./resources/img/maps/"))


# --- Classes ---

class ImageMetadata:
    """Represents the metadata of a single image."""
    def __init__(self, metadata: list):
        self.filename: str = metadata[0]
        self.name: str = metadata[1]
        self.long_name: str = metadata[2]
        self.description: str = metadata[3]
        self.source: str = metadata[4]
        self.emoji: str = metadata[5]


class ImagesGroup(collections.abc.Mapping):
    """Represents a group of images, loaded from a meta.json file."""
    def __init__(self, file_path):
        self._images = {}
        self.path = file_path

        with open(file_path, "r") as file:
            images: dict = json.load(file)
        for key, imgdata in images.items():
            self._images[key] = ImageMetadata(imgdata)

    # Wrappers to implement dict-like functionality
    def __len__(self):
        return len(self._images)

    def __getitem__(self, key: str):
        return self._images[key]

    def __iter__(self):
        return iter(self._images)

    # str(): Simply return what it would be for the underlaying dict
    def __str__(self):
        return str(self._images)


# --- Helper functions ---

def embed_factory(ctx: commands.Context) -> discord.Embed:
    """Creates an embed with neutral colour and standard footer."""
    embed = discord.Embed(timestamp=datetime.utcnow(), colour=colours.neutral)
    embed.set_footer(text=ctx.author, icon_url=str(ctx.author.avatar_url))
    return embed


def error_embed_factory(ctx: commands.Context, exception: Exception, debug_mode: bool) -> discord.Embed:
    """Creates an Error embed."""
    if debug_mode:
        fmtd_ex = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    else:
        fmtd_ex = traceback.format_exception_only(exception.__class__, exception)
    embed = embed_factory(ctx)
    embed.title = "Error"
    embed.description = "```\n" + '\n'.join(fmtd_ex) + "```"
    embed.colour = colours.bad
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
