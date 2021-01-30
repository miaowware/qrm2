"""
ae7q extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


# Test callsigns:
# KN8U: active, restricted
# AB2EE: expired, restricted
# KE8FGB: assigned once, no restrictions
# KV4AAA: unassigned, no records
# KC4USA: reserved, no call history, *but* has application history


import aiohttp
from bs4 import BeautifulSoup

import discord.ext.commands as commands

import common as cmn


class AE7QCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.group(name="ae7q", aliases=["ae"], case_insensitive=True, category=cmn.cat.lookup)
    async def _ae7q_lookup(self, ctx: commands.Context):
        """Looks up a callsign, FRN, or Licensee ID on [ae7q.com](http://ae7q.com/)."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_ae7q_lookup.command(name="call", aliases=["c"], category=cmn.cat.lookup)
    async def _ae7q_call(self, ctx: commands.Context, callsign: str):
        """Looks up the history of a callsign on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            callsign = callsign.upper()
            desc = ""
            base_url = "http://ae7q.com/query/data/CallHistory.php?CALL="
            embed = cmn.embed_factory(ctx)

            if not callsign.isalnum():
                embed = cmn.embed_factory(ctx)
                embed.title = "AE7Q History for Callsign"
                embed.colour = cmn.colours.bad
                embed.description = "Not a valid callsign!"
                await ctx.send(embed=embed)
                return

            async with self.session.get(base_url + callsign) as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                page = await resp.text()

            soup = BeautifulSoup(page, features="html.parser")
            tables = [[row for row in table.find_all("tr")] for table in soup.select("table.Database")]

            table = tables[0]

            # find the first table in the page, and use it to make a description
            if len(table[0]) == 1:
                for row in table:
                    desc += " ".join(row.getText().split())
                    desc += "\n"
                desc = desc.replace(callsign, f"`{callsign}`")
                table = tables[1]

            table_headers = table[0].find_all("th")
            first_header = "".join(table_headers[0].strings) if len(table_headers) > 0 else None

            # catch if the wrong table was selected
            if first_header is None or first_header != "Entity Name":
                embed.title = f"AE7Q History for {callsign}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + callsign
                embed.description = desc
                embed.description += f"\nNo records found for `{callsign}`"
                await ctx.send(embed=embed)
                return

            table = await process_table(table[1:])

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q History for {callsign}"
            embed.colour = cmn.colours.good
            embed.url = base_url + callsign

            # add the first three rows of the table to the embed
            for row in table[0:3]:
                header = f"**{row[0]}** ({row[1]})"     # **Name** (Applicant Type)
                body = (f"Class: *{row[2]}*\n"
                        f"Region: *{row[3]}*\n"
                        f"Status: *{row[4]}*\n"
                        f"Granted: *{row[5]}*\n"
                        f"Effective: *{row[6]}*\n"
                        f"Cancelled: *{row[7]}*\n"
                        f"Expires: *{row[8]}*")
                embed.add_field(name=header, value=body, inline=False)

            if len(table) > 3:
                desc += f"\nRecords 1 to 3 of {len(table)}. See ae7q.com for more..."

            embed.description = desc

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="trustee", aliases=["t"], category=cmn.cat.lookup)
    async def _ae7q_trustee(self, ctx: commands.Context, callsign: str):
        """Looks up the licenses for which a licensee is trustee on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            callsign = callsign.upper()
            desc = ""
            base_url = "http://ae7q.com/query/data/CallHistory.php?CALL="
            embed = cmn.embed_factory(ctx)

            if not callsign.isalnum():
                embed = cmn.embed_factory(ctx)
                embed.title = "AE7Q Trustee History for Callsign"
                embed.colour = cmn.colours.bad
                embed.description = "Not a valid callsign!"
                await ctx.send(embed=embed)
                return

            async with self.session.get(base_url + callsign) as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                page = await resp.text()

            soup = BeautifulSoup(page, features="html.parser")
            tables = [[row for row in table.find_all("tr")] for table in soup.select("table.Database")]

            try:
                table = tables[2] if len(tables[0][0]) == 1 else tables[1]
            except IndexError:
                embed.title = f"AE7Q Trustee History for {callsign}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + callsign
                embed.description = desc
                embed.description += f"\nNo records found for `{callsign}`"
                await ctx.send(embed=embed)
                return

            table_headers = table[0].find_all("th")
            first_header = "".join(table_headers[0].strings) if len(table_headers) > 0 else None

            # catch if the wrong table was selected
            if first_header is None or not first_header.startswith("With"):
                embed.title = f"AE7Q Trustee History for {callsign}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + callsign
                embed.description = desc
                embed.description += f"\nNo records found for `{callsign}`"
                await ctx.send(embed=embed)
                return

            table = await process_table(table[2:])

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q Trustee History for {callsign}"
            embed.colour = cmn.colours.good
            embed.url = base_url + callsign

            # add the first three rows of the table to the embed
            for row in table[0:3]:
                header = f"**{row[0]}** ({row[3]})"     # **Name** (Applicant Type)
                body = (f"Name: *{row[2]}*\n"
                        f"Region: *{row[1]}*\n"
                        f"Status: *{row[4]}*\n"
                        f"Granted: *{row[5]}*\n"
                        f"Effective: *{row[6]}*\n"
                        f"Cancelled: *{row[7]}*\n"
                        f"Expires: *{row[8]}*")
                embed.add_field(name=header, value=body, inline=False)

            if len(table) > 3:
                desc += f"\nRecords 1 to 3 of {len(table)}. See ae7q.com for more..."

            embed.description = desc

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="applications", aliases=["a"], category=cmn.cat.lookup)
    async def _ae7q_applications(self, ctx: commands.Context, callsign: str):
        """Looks up the application history for a callsign on [ae7q.com](http://ae7q.com/)."""
        """
        with ctx.typing():
            callsign = callsign.upper()
            desc = ""
            base_url = "http://ae7q.com/query/data/CallHistory.php?CALL="
            embed = cmn.embed_factory(ctx)

            if not callsign.isalnum():
                embed = cmn.embed_factory(ctx)
                embed.title = "AE7Q Application History for Callsign"
                embed.colour = cmn.colours.bad
                embed.description = "Not a valid callsign!"
                await ctx.send(embed=embed)
                return

            async with self.session.get(base_url + callsign) as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                page = await resp.text()

            soup = BeautifulSoup(page, features="html.parser")
            tables = [[row for row in table.find_all("tr")] for table in soup.select("table.Database")]

            table = tables[0]

            # find the first table in the page, and use it to make a description
            if len(table[0]) == 1:
                for row in table:
                    desc += " ".join(row.getText().split())
                    desc += "\n"
                desc = desc.replace(callsign, f"`{callsign}`")

            # select the last table to get applications
            table = tables[-1]

            table_headers = table[0].find_all("th")
            first_header = "".join(table_headers[0].strings) if len(table_headers) > 0 else None

            # catch if the wrong table was selected
            if first_header is None or not first_header.startswith("Receipt"):
                embed.title = f"AE7Q Application History for {callsign}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + callsign
                embed.description = desc
                embed.description += f"\nNo records found for `{callsign}`"
                await ctx.send(embed=embed)
                return

            table = await process_table(table[1:])

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q Application History for {callsign}"
            embed.colour = cmn.colours.good
            embed.url = base_url + callsign

            # add the first three rows of the table to the embed
            for row in table[0:3]:
                header = f"**{row[1]}** ({row[3]})"     # **Name** (Callsign)
                body = (f"Received: *{row[0]}*\n"
                        f"Region: *{row[2]}*\n"
                        f"Purpose: *{row[5]}*\n"
                        f"Last Action: *{row[7]}*\n"
                        f"Application Status: *{row[8]}*\n")
                embed.add_field(name=header, value=body, inline=False)

            if len(table) > 3:
                desc += f"\nRecords 1 to 3 of {len(table)}. See ae7q.com for more..."

            embed.description = desc

            await ctx.send(embed=embed)
        """
        raise NotImplementedError("Application history lookup not yet supported. "
                                  "Check back in a later version of the bot.")

    @_ae7q_lookup.command(name="frn", aliases=["f"], category=cmn.cat.lookup)
    async def _ae7q_frn(self, ctx: commands.Context, frn: str):
        """Looks up the history of an FRN on [ae7q.com](http://ae7q.com/)."""
        """
        NOTES:
        - 2 tables: callsign history and application history
        - If not found: no tables
        """
        with ctx.typing():
            base_url = "http://ae7q.com/query/data/FrnHistory.php?FRN="
            embed = cmn.embed_factory(ctx)

            if not frn.isdecimal():
                embed = cmn.embed_factory(ctx)
                embed.title = "AE7Q History for FRN"
                embed.colour = cmn.colours.bad
                embed.description = "Not a valid FRN!"
                await ctx.send(embed=embed)
                return

            async with self.session.get(base_url + frn) as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                page = await resp.text()

            soup = BeautifulSoup(page, features="html.parser")
            tables = [[row for row in table.find_all("tr")] for table in soup.select("table.Database")]

            if not len(tables):
                embed.title = f"AE7Q History for FRN {frn}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + frn
                embed.description = f"No records found for FRN `{frn}`"
                await ctx.send(embed=embed)
                return

            table = tables[0]

            table_headers = table[0].find_all("th")
            first_header = "".join(table_headers[0].strings) if len(table_headers) > 0 else None

            # catch if the wrong table was selected
            if first_header is None or not first_header.startswith("With Licensee"):
                embed.title = f"AE7Q History for FRN {frn}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + frn
                embed.description = f"No records found for FRN `{frn}`"
                await ctx.send(embed=embed)
                return

            table = await process_table(table[2:])

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q History for FRN {frn}"
            embed.colour = cmn.colours.good
            embed.url = base_url + frn

            # add the first three rows of the table to the embed
            for row in table[0:3]:
                header = f"**{row[0]}** ({row[3]})"     # **Callsign** (Applicant Type)
                body = (f"Name: *{row[2]}*\n"
                        f"Class: *{row[4]}*\n"
                        f"Region: *{row[1]}*\n"
                        f"Status: *{row[5]}*\n"
                        f"Granted: *{row[6]}*\n"
                        f"Effective: *{row[7]}*\n"
                        f"Cancelled: *{row[8]}*\n"
                        f"Expires: *{row[9]}*")
                embed.add_field(name=header, value=body, inline=False)

            if len(table) > 3:
                embed.description = f"Records 1 to 3 of {len(table)}. See ae7q.com for more..."

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="licensee", aliases=["l"], category=cmn.cat.lookup)
    async def _ae7q_licensee(self, ctx: commands.Context, licensee_id: str):
        """Looks up the history of a licensee ID on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            licensee_id = licensee_id.upper()
            base_url = "http://ae7q.com/query/data/LicenseeIdHistory.php?ID="
            embed = cmn.embed_factory(ctx)

            if not licensee_id.isalnum():
                embed = cmn.embed_factory(ctx)
                embed.title = "AE7Q History for Licensee"
                embed.colour = cmn.colours.bad
                embed.description = "Not a valid licensee ID!"
                await ctx.send(embed=embed)
                return

            async with self.session.get(base_url + licensee_id) as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                page = await resp.text()

            soup = BeautifulSoup(page, features="html.parser")
            tables = [[row for row in table.find_all("tr")] for table in soup.select("table.Database")]

            if not len(tables):
                embed.title = f"AE7Q History for Licensee {licensee_id}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + licensee_id
                embed.description = f"No records found for Licensee `{licensee_id}`"
                await ctx.send(embed=embed)
                return

            table = tables[0]

            table_headers = table[0].find_all("th")
            first_header = "".join(table_headers[0].strings) if len(table_headers) > 0 else None

            # catch if the wrong table was selected
            if first_header is None or not first_header.startswith("With FCC"):
                embed.title = f"AE7Q History for Licensee {licensee_id}"
                embed.colour = cmn.colours.bad
                embed.url = base_url + licensee_id
                embed.description = f"No records found for Licensee `{licensee_id}`"
                await ctx.send(embed=embed)
                return

            table = await process_table(table[2:])

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q History for Licensee {licensee_id}"
            embed.colour = cmn.colours.good
            embed.url = base_url + licensee_id

            # add the first three rows of the table to the embed
            for row in table[0:3]:
                header = f"**{row[0]}** ({row[3]})"     # **Callsign** (Applicant Type)
                body = (f"Name: *{row[2]}*\n"
                        f"Class: *{row[4]}*\n"
                        f"Region: *{row[1]}*\n"
                        f"Status: *{row[5]}*\n"
                        f"Granted: *{row[6]}*\n"
                        f"Effective: *{row[7]}*\n"
                        f"Cancelled: *{row[8]}*\n"
                        f"Expires: *{row[9]}*")
                embed.add_field(name=header, value=body, inline=False)

            if len(table) > 3:
                embed.description = f"Records 1 to 3 of {len(table)}. See ae7q.com for more..."

            await ctx.send(embed=embed)


async def process_table(table: list):
    """Processes tables (*not* including headers) and returns the processed table"""
    table_contents = []
    for tr in table:
        row = []
        for td in tr.find_all("td"):
            cell_val = td.getText().strip()
            row.append(cell_val if cell_val else "-")

            # take care of columns that span multiple rows by copying the contents rightward
            if "colspan" in td.attrs and int(td.attrs["colspan"]) > 1:
                for i in range(int(td.attrs["colspan"]) - 1):
                    row.append(row[-1])

        # get rid of ditto marks by copying the contents from the previous row
        for i, cell in enumerate(row):
            if cell == "\"":
                row[i] = table_contents[-1][i]
        # add row to table
        table_contents += [row]
    return table_contents


def setup(bot: commands.Bot):
    bot.add_cog(AE7QCog(bot))
