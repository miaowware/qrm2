"""
TeX extension for qrm
---
Copyright (C) 2021 classabbyamp, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import aiohttp
from io import BytesIO
from urllib.parse import urljoin

import discord
import discord.ext.commands as commands

import common as cmn
import data.options as opt


class TexCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)
        with open(cmn.paths.resources / "template.1.tex") as latex_template:
            self.template = latex_template.read()

    @commands.command(name="tex", aliases=["latex"], category=cmn.Cats.UTILS)
    async def tex(self, ctx: commands.Context, *, expr: str):
        """Renders a LaTeX expression.

        In paragraph mode by default. To render math, add `$` around math expressions.
        """
        payload = {
            "format": "png",
            "code": self.template.replace("#CONTENT#", expr),
            "quality": 50
        }

        with ctx.typing():
            # ask rTeX to render our expression
            async with self.session.post(urljoin(opt.rtex_instance, "api/v2"), json=payload) as r:
                if r.status != 200:
                    raise cmn.BotHTTPError(r)

                render_result = await r.json()
                if render_result["status"] != "success":
                    embed = cmn.embed_factory(ctx)
                    embed.title = "LaTeX Rendering Failed!"
                    embed.description = ("Here are some common reasons:\n"
                                         "• Did you forget to use math mode? Surround math expressions with `$`,"
                                         " like `$x^3$`.\n"
                                         "• Are you using a command from a package? It might not be available.\n"
                                         "• Are you including the document headers? We already did that for you.")
                    embed.colour = cmn.colours.bad
                    await ctx.send(embed=embed)
                    return

            # if rendering went well, download the file given in the response
            async with self.session.get(urljoin(opt.rtex_instance, "api/v2/" + render_result["filename"])) as r:
                png_buffer = BytesIO(await r.read())

            embed = cmn.embed_factory(ctx)
            embed.title = "LaTeX Expression"
            embed.description = "Rendered by [rTeX](https://rtex.probablyaweb.site/)."
            embed.set_image(url="attachment://tex.png")
            await ctx.send(file=discord.File(png_buffer, "tex.png"), embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(TexCog(bot))
