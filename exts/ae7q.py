"""
ae7q extension for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
---
Test callsigns:
KN8U: active, restricted
AB2EE: expired, restricted
KE8FGB: assigned once, no restrictions
NA2AAA: unassigned, no records
"""

from datetime import datetime

import discord
import discord.ext.commands as commands

from bs4 import BeautifulSoup
import aiohttp

import common as cmn


class AE7QCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="ae7q", aliases=["ae"], category=cmn.cat.lookup)
    async def _ae7q_lookup(self, ctx: commands.Context):
        '''Look up a callsign, FRN, or Licensee ID on [ae7q.com](http://ae7q.com/).'''
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_ae7q_lookup.command(name="call", category=cmn.cat.lookup)
    async def _ae7q_call(self, ctx: commands.Context, callsign: str):
        '''Look up the history for a callsign on [ae7q.com](http://ae7q.com/).'''
        callsign = callsign.upper()
        desc = ''
        base_url = "http://ae7q.com/query/data/CallHistory.php?CALL="

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + callsign) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not load AE7Q')
                page = await resp.text()

        soup = BeautifulSoup(page, features="html.parser")
        tables = soup.select("table.Database")

        for table in tables:
            rows = table.find_all("tr")
            if len(rows) > 1 and len(rows[0]) > 1:
                break
            if desc == '':
                for row in rows:
                    desc += " ".join(row.getText().split())
                    desc += '\n'
                desc = desc.replace(callsign, f'`{callsign}`')
            rows = None

        if rows is None:
            embed = discord.Embed(title=f"AE7Q History for {callsign}",
                                  colour=cmn.colours.bad,
                                  url=f"{base_url}{callsign}",
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
            embed.description = desc
            embed.description += f'\nNo records found for `{callsign}`'
            await ctx.send(embed=embed)
            return

        table_contents = []  # store your table here
        for tr in rows:
            if rows.index(tr) == 0:
                continue
            row_cells = []
            for td in tr.find_all('td'):
                if td.getText().strip() != '':
                    row_cells.append(td.getText().strip())
                else:
                    row_cells.append('-')
                if 'colspan' in td.attrs and int(td.attrs['colspan']) > 1:
                    for i in range(int(td.attrs['colspan']) - 1):
                        row_cells.append(row_cells[-1])
            for i, cell in enumerate(row_cells):
                if cell == '"':
                    cell = table_contents[-1][i]
            if len(row_cells) > 1:
                table_contents += [row_cells]

        embed = discord.Embed(title=f"AE7Q Records for {callsign}",
                              colour=cmn.colours.good,
                              url=f"{base_url}{callsign}",
                              timestamp=datetime.utcnow())

        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))

        for row in table_contents[0:3]:
            header = f'**{row[0]}** ({row[1]})'
            body = f'Class: *{row[2]}*\n'
            body += f'Region: *{row[3]}*\n'
            body += f'Status: *{row[4]}*\n'
            body += f'Granted: *{row[5]}*\n'
            body += f'Effective: *{row[6]}*\n'
            body += f'Cancelled: *{row[7]}*\n'
            body += f'Expires: *{row[8]}*'
            embed.add_field(name=header, value=body, inline=False)

        embed.description = desc
        if len(table_contents) > 3:
            embed.description += f'\nRecords 1 to 3 of {len(table_contents)}.'
            embed.description += ' See ae7q.com for more...'

        await ctx.send(embed=embed)

    # TODO: write commands for other AE7Q response types?
    # @_ae7q_lookup.command(name="trustee")
    # async def _ae7q_trustee(self, ctx: commands.Context, callsign: str):
    #     pass

    # @_ae7q_lookup.command(name="applications", aliases=['apps'])
    # async def _ae7q_applications(self, ctx: commands.Context, callsign: str):
    #     pass

    # @_ae7q_lookup.command(name="frn")
    # async def _ae7q_frn(self, ctx: commands.Context, frn: str):
    #     base_url = "http://ae7q.com/query/data/FrnHistory.php?FRN="
    #     pass

    # @_ae7q_lookup.command(name="licensee", aliases=["lic"])
    # async def _ae7q_licensee(self, ctx: commands.Context, frn: str):
    #     base_url = "http://ae7q.com/query/data/LicenseeIdHistory.php?ID="
    #     pass


def setup(bot: commands.Bot):
    bot.add_cog(AE7QCog(bot))
