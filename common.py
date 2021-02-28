"""
Common tools for the bot.
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import collections
import json
import re
import traceback
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Union

import aiohttp

import discord
import discord.ext.commands as commands
from discord import Emoji, Reaction, PartialEmoji

import data.options as opt


__all__ = ["colours", "cat", "emojis", "paths", "ImageMetadata", "ImagesGroup",
           "embed_factory", "error_embed_factory", "add_react", "check_if_owner"]


# --- Common values ---

colours = SimpleNamespace(
    good=0x43B581,
    neutral=0x7289DA,
    bad=0xF04747,
    timeout=0xF26522,
)

# meow
cat = SimpleNamespace(
    lookup="Information Lookup",
    fun="Fun",
    maps="Mapping",
    ref="Reference",
    study="Exam Study",
    weather="Land and Space Weather",
    admin="Bot Control",
)

emojis = SimpleNamespace(
    check_mark="✅",
    x="❌",
    warning="⚠️",
    question="❓",
    no_entry="⛔",
    bangbang="‼️",
    clock="⏱",
    a="🇦",
    b="🇧",
    c="🇨",
    d="🇩",
    e="🇪",
)

paths = SimpleNamespace(
    data=Path("./data/"),
    resources=Path("./resources/"),
    img=Path("./resources/img/"),
    bandcharts=Path("./resources/img/bandcharts/"),
    maps=Path("./resources/img/maps/"),
)


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


# --- Exceptions ---

class BotHTTPError(Exception):
    """Raised whan a requests fails (status != 200) in a command."""
    def __init__(self, response: aiohttp.ClientResponse):
        msg = f"Request failed: {response.status} {response.reason}"
        super().__init__(msg)
        self.response = response
        self.status = response.status
        self.reason = response.reason


# --- Converters ---

class GlobalChannelConverter(commands.IDConverter):
    """Converter to get any bot-acessible channel by ID/mention (global), or name (in current guild only)."""
    async def convert(self, ctx: commands.Context, argument: str):
        bot = ctx.bot
        guild = ctx.guild
        match = self._get_id_match(argument) or re.match(r"<#([0-9]+)>$", argument)
        result = None
        if match is None:
            # not a mention/ID
            if guild:
                result = discord.utils.get(guild.text_channels, name=argument)
            else:
                raise commands.BadArgument(f"""Channel named "{argument}" not found in this guild.""")
        else:
            channel_id = int(match.group(1))
            result = bot.get_channel(channel_id)
        if not isinstance(result, (discord.TextChannel, discord.abc.PrivateChannel)):
            raise commands.BadArgument(f"""Channel "{argument}" not found.""")
        return result


# --- Helper functions ---

def embed_factory(ctx: commands.Context) -> discord.Embed:
    """Creates an embed with neutral colour and standard footer."""
    embed = discord.Embed(timestamp=datetime.utcnow(), colour=colours.neutral)
    embed.set_footer(text=str(ctx.author), icon_url=str(ctx.author.avatar_url))
    return embed


def error_embed_factory(ctx: commands.Context, exception: Exception, debug_mode: bool) -> discord.Embed:
    """Creates an Error embed."""
    if debug_mode:
        fmtd_ex = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    else:
        fmtd_ex = traceback.format_exception_only(exception.__class__, exception)
    embed = embed_factory(ctx)
    embed.title = "⚠️ Error"
    embed.description = "```\n" + "\n".join(fmtd_ex) + "```"
    embed.colour = colours.bad
    return embed


async def add_react(msg: discord.Message, react: Union[Emoji, Reaction, PartialEmoji, str]):
    try:
        await msg.add_reaction(react)
    except discord.Forbidden:
        idpath = (f"{msg.guild.id}/" if msg.guild else "") + str(msg.channel.id)
        print(f"[!!] Missing permissions to add reaction in '{idpath}'!")


# --- Checks ---

async def check_if_owner(ctx: commands.Context):
    if ctx.author.id in opt.owners_uids:
        return True
    raise commands.NotOwner
