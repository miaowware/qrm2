"""
ae7q cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import discord
import discord.ext.commands as commands

from datetime import datetime
from bs4 import BeautifulSoup
import aiohttp


class AE7QCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.group(name="ae7q", aliases=["ae"])
    async def _ae7q_lookup(self, ctx):
        '''Look up a callsign, FRN, or Licensee ID on ae7q.com'''
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid ae7q command passed\nPossible commands:' +
                           '`call`, `frn`, `lic` or `licensee`.')

    @_ae7q_lookup.command(name="call")
    async def _ae7q_call(self, ctx, callsign: str):
        callsign = callsign.upper()
        base_url = "http://ae7q.com/query/data/CallHistory.php?CALL="

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + callsign) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not load AE7Q')
                page = await resp.text()

        soup = BeautifulSoup(page, features="html.parser")
        table = soup.select("table.Database")[1]

        rows = table.find_all("tr")
        table_contents = []  # store your table here
        for tr in rows:
            if rows.index(tr) == 0:
                continue
            else:
                row_cells = []
                for td in tr.find_all('td'):
                    if td.getText().strip() != '':
                        row_cells.append(td.getText().strip())
                    else:
                        row_cells.append('-')
                    if 'colspan' in td.attrs and int(td.attrs['colspan']) > 1:
                        for i in range(int(td.attrs['colspan']) - 1):
                            row_cells.append(row_cells[-1])
                for i in range(len(row_cells)):
                    if row_cells[i] == '"':
                        row_cells[i] = table_contents[-1][i]
            if len(row_cells) > 1:
                table_contents += [row_cells]

        embed = discord.Embed(title=f"AE7Q History for {callsign}",
                              colour=self.gs.colours.good,
                              url=f"{base_url}{callsign}",
                              timestamp=datetime.utcnow())

        embed.set_author(name=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))

        for row in table_contents:
            embed.add_field(name=row[0], value=row[1], inline=False)
            embed.add_field(name="Class", value=row[2], inline=True)
            embed.add_field(name="Region", value=row[3], inline=True)
            embed.add_field(name="Status", value=row[4], inline=True)
            embed.add_field(name="Grant", value=row[5], inline=True)
            embed.add_field(name="Effective", value=row[6], inline=True)
            embed.add_field(name="Cancel", value=row[7], inline=True)
            embed.add_field(name="Expire", value=row[8], inline=True)

        await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="frn")
    async def _ae7q_frn(self, ctx, frn: str):
        base_url = "http://ae7q.com/query/data/FrnHistory.php?FRN="
        pass

    @_ae7q_lookup.command(name="licensee", aliases=["lic"])
    async def _ae7q_licensee(self, ctx, frn: str):
        base_url = "http://ae7q.com/query/data/LicenseeIdHistory.php?ID="
        pass


def setup(bot):
    bot.add_cog(AE7QCog(bot))
