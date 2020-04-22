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


import re

import aiohttp
import ae7qparser

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

            call_data = ae7qparser.get_call(callsign)

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q Callsign History for {callsign}"
            embed.url = call_data.query_url
            embed.colour = cmn.colours.good
            embed.description = ""

            if isinstance(call_data, ae7qparser.Ae7qCallData):
                if call_data.conditions:
                    embed.description = " ".join([
                                                    " ".join([y.strip() for y in x]) for x in call_data.conditions
                                                 ]).replace(callsign, f"`{callsign}`")

                if not call_data.call_history:
                    if not call_data.event_callsign_history:
                        embed.colour = cmn.colours.bad
                        embed.description += f"\nNo records found for `{callsign}`"
                    else:
                        # add the first five rows of the event callsign history to the embed
                        for row in call_data.event_callsign_history[0:5]:
                            header = f"**{row.start_date:%Y-%m-%d}-{row.end_date:%Y-%m-%d}**"
                            body = (f"Requestor: *{row.entity_name} ({row.callsign})*\n"
                                    f"Event: *{row.event_name}*")
                            embed.add_field(name=header, value=body, inline=False)

                        if len(call_data.event_callsign_history) > 5:
                            embed.description += (f"\nRecords 1 to 5 of {len(call_data.event_callsign_history)}. "
                                                  f"See [ae7q.com]({call_data.query_url}) for more...")

                else:
                    # add the first three rows of the callsign history to the embed
                    for row in call_data.call_history[0:3]:
                        header = f"**{row.entity_name}** ({row.applicant_type})"
                        body = (f"Class: *{row.operator_class}*\n"
                                f"Region: *{row.region_state}*\n"
                                f"Status: *{row.license_status}*\n")
                        if row.grant_date:
                            body += f"Granted: *{row.grant_date:%Y-%m-%d}*\n"
                        if row.effective_date:
                            body += f"Effective: *{row.effective_date:%Y-%m-%d}*\n"
                        if row.cancel_date:
                            body += f"Cancelled: *{row.cancel_date:%Y-%m-%d}*\n"
                        if row.expire_date:
                            body += f"Expires: *{row.expire_date:%Y-%m-%d}*\n"

                        embed.add_field(name=header, value=body, inline=False)

                    if len(call_data.call_history) > 3:
                        embed.description += (f"\nRecords 1 to 3 of {len(call_data.call_history)}. "
                                              f"See [ae7q.com]({call_data.query_url}) for more...")

            elif isinstance(call_data, ae7qparser.Ae7qCanadianCallData):
                if not call_data.callsign_data:
                    embed.colour = cmn.colours.bad
                    embed.description += f"\nNo records found for `{callsign}`"
                else:
                    if call_data.given_names != "" and call_data.surname != "":
                        embed.add_field(name="Name", value=f"{call_data.given_names} {call_data.surname}", inline=True)
                    if call_data.address != "":
                        embed.add_field(name="Address", value=call_data.address, inline=True)
                    if call_data.locality != "":
                        embed.add_field(name="Locality", value=call_data.locality, inline=True)
                    if call_data.province != "":
                        embed.add_field(name="Province", value=call_data.province, inline=True)
                    if call_data.postal_code != "":
                        embed.add_field(name="Postal Code", value=call_data.postal_code, inline=True)
                    if call_data.country != "":
                        embed.add_field(name="Country", value=call_data.country, inline=True)
                    if call_data.region != "":
                        embed.add_field(name="Region", value=call_data.region, inline=True)
                    if call_data.grid_square != "":
                        embed.add_field(name="Grid Square", value=call_data.grid_square, inline=True)
                    if call_data.qualifications != "":
                        embed.add_field(name="License Qualifications", value=call_data.qualifications, inline=True)

            else:
                embed.colour = cmn.colours.bad
                embed.description += f"\nNo records found for `{callsign}`"

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="trustee", aliases=["t"], category=cmn.cat.lookup)
    async def _ae7q_trustee(self, ctx: commands.Context, callsign: str):
        """Looks up the licenses for which a licensee is trustee on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            callsign = callsign.upper()

            call_data = ae7qparser.get_call(callsign)

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q Trustee History for {callsign}"
            embed.url = call_data.query_url
            embed.colour = cmn.colours.good
            embed.description = ""

            if isinstance(call_data, ae7qparser.Ae7qCallData):
                if not call_data.trustee_history:
                    embed.colour = cmn.colours.bad
                    embed.description += f"\nNo records found for `{callsign}`"
                else:
                    # add the first three rows of the trustee history to the embed
                    for row in call_data.trustee_history[0:3]:
                        header = f"**{row.callsign}** ({row.applicant_type})"
                        body = (f"Name: *{row.entity_name}*\n"
                                f"Region: *{row.region_state}*\n"
                                f"Status: *{row.license_status}*\n")
                        if row.grant_date:
                            body += f"Granted: *{row.grant_date:%Y-%m-%d}*\n"
                        if row.effective_date:
                            body += f"Effective: *{row.effective_date:%Y-%m-%d}*\n"
                        if row.cancel_date:
                            body += f"Cancelled: *{row.cancel_date:%Y-%m-%d}*\n"
                        if row.expire_date:
                            body += f"Expires: *{row.expire_date:%Y-%m-%d}*\n"

                        embed.add_field(name=header, value=body, inline=False)

                    if len(call_data.trustee_history) > 3:
                        embed.description += (f"\nRecords 1 to 3 of {len(call_data.trustee_history)}. "
                                              f"See [ae7q.com]({call_data.query_url}) for more...")

            else:
                embed.colour = cmn.colours.bad
                embed.description += f"\nNo records found for `{callsign}`"

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="applications", aliases=["a", "apps"], category=cmn.cat.lookup)
    async def _ae7q_applications(self, ctx: commands.Context, query: str):
        """Looks up the application history for a callsign, FRN, or Licensee ID on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            query = query.upper()

            # LID
            if re.match(r"L\d+", query):
                data = ae7qparser.get_licensee_id(query)
            # FRN
            elif re.match(r"\d{10}", query):
                data = ae7qparser.get_frn(query)
            # callsign
            else:
                data = ae7qparser.get_call(query)

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q Application History for {query}"
            embed.url = data.query_url
            embed.colour = cmn.colours.good
            embed.description = ""

            if not data.application_history:
                embed.colour = cmn.colours.bad
                embed.description += f"\nNo records found for `{query}`"
            else:
                # add the first three rows of the app history to the embed
                if isinstance(data.application_history, ae7qparser.ApplicationsHistoryTable):
                    for row in data.application_history[0:3]:
                        header = f"**{row.uls_file_number[0]}** ({row.receipt_date:%Y-%m-%d})"
                        body = (f"Name: *{row.entity_name}*\n"
                                f"Callsign: *{row.application_callsign}*\n"
                                f"Region: *{row.region_state}*\n"
                                f"Purpose: *{row.application_purpose}*\n")
                        if row.payment_date:
                            body += f"Payment: *{row.payment_date:%Y-%m-%d}*\n"
                        if row.last_action_date:
                            body += f"Last Action: *{row.last_action_date:%Y-%m-%d}*\n"
                        body += f"Status: *{row.application_status}*"
                        embed.add_field(name=header, value=body, inline=False)

                elif isinstance(data.application_history, ae7qparser.VanityApplicationsHistoryTable):
                    for row in data.application_history[0:3]:
                        header = f"**{row.uls_file_number[0]}** ({row.receipt_date:%Y-%m-%d})"
                        body = (f"Callsign: *{row.application_callsign}*\n"
                                f"Region: *{row.region_state}*\n"
                                f"Operator Class: *{row.operator_class}*\n"
                                f"Purpose: *{row.application_purpose}*\n")
                        if row.payment_date:
                            body += f"Payment: *{row.payment_date:%Y-%m-%d}*\n"
                        if row.last_action_date:
                            body += f"Last Action: *{row.last_action_date:%Y-%m-%d}*\n"
                        body += f"Status: *{row.application_status}*\n"
                        if row.applied_callsigns:
                            body += (f"Callsign{'s' if len(row.applied_callsigns) > 1 else ''} "
                                     f"Applied For: *{', '.join(row.applied_callsigns)}*")
                        embed.add_field(name=header, value=body, inline=False)

                if len(data.application_history) > 3:
                    embed.description += (f"\nRecords 1 to 3 of {len(data.application_history)}. "
                                          f"See [ae7q.com]({data.query_url}) for more...")

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="pending_apps", aliases=["pa"], category=cmn.cat.lookup)
    async def _ae7q_pending_applications(self, ctx: commands.Context, query: str):
        """Looks up the pending applications for a callsign, FRN, or Licensee ID on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            query = query.upper()

            # LID
            if re.match(r"L\d+", query):
                data = ae7qparser.get_licensee_id(query)
            # FRN
            elif re.match(r"\d{10}", query):
                data = ae7qparser.get_frn(query)
            # callsign
            else:
                data = ae7qparser.get_call(query)

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q Pending Applications for {query}"
            embed.url = data.query_url
            embed.colour = cmn.colours.good
            embed.description = ""

            if not data.pending_applications:
                embed.colour = cmn.colours.bad
                embed.description += f"\nNo records found for `{query}`"
            else:
                # add the first three rows of the pending apps to the embed
                if isinstance(data.pending_applications, ae7qparser.PendingApplicationsPredictionsTable):
                    for row in data.pending_applications[0:3]:
                        header = f"**{row.uls_file_number}** ({row.receipt_date:%Y-%m-%d})"
                        body = (f"Callsign: *{row.applicant_callsign}*\n"
                                f"Region: *{row.region_state}*\n"
                                f"Operator Class: *{row.operator_class}*\n"
                                f"Vanity Type: *{row.vanity_type}*\n")
                        if row.process_date:
                            body += f"Processes On: *{row.process_date:%Y-%m-%d}*\n"
                        body += (f"Sequential #: *{row.sequential_number}*\n"
                                 f"Vanity Callsign: *{row.vanity_callsign}*\n"
                                 f"Prediction: *{row.prediction}*")
                        embed.add_field(name=header, value=body, inline=False)

                elif isinstance(data.pending_applications, ae7qparser.CallsignPendingApplicationsPredictionsTable):
                    for row in data.pending_applications[0:3]:
                        header = f"**{row.uls_file_number}** ({row.receipt_date:%Y-%m-%d})"
                        body = (f"Callsign: *{row.applicant_callsign}*\n"
                                f"Region: *{row.region_state}*\n"
                                f"Operator Class: *{row.operator_class}*\n"
                                f"Vanity Type: *{row.vanity_type}*\n")
                        if row.process_date:
                            body += f"Processes On: *{row.process_date:%Y-%m-%d}*\n"
                        body += (f"Sequential #: *{row.sequential_number}*\n"
                                 f"Prediction: *{row.prediction}*")
                        embed.add_field(name=header, value=body, inline=False)

                if len(data.pending_applications) > 3:
                    embed.description += (f"\nRecords 1 to 3 of {len(data.pending_applications)}. "
                                          f"See [ae7q.com]({data.query_url}) for more...")

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="app_detail", aliases=["ad"], category=cmn.cat.lookup)
    async def _ae7q_app_detail(self, ctx: commands.Context, ufn: str):
        """Looks up the application data for a ULS file number on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            app_data = ae7qparser.get_application(ufn)

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q Application Data for {ufn}"
            embed.url = app_data.query_url
            embed.colour = cmn.colours.good

            if not app_data.application_data:
                embed.colour = cmn.colours.bad
                embed.description += f"\nNo records found for `{ufn}`"
            else:
                if app_data.frn:
                    embed.add_field(name="FRN", value=app_data.frn, inline=True)
                if app_data.licensee_id:
                    embed.add_field(name="Licensee ID", value=app_data.licensee_id, inline=True)
                if app_data.applicant_type:
                    embed.add_field(name="Applicant Type", value=app_data.applicant_type, inline=True)
                if app_data.entity_type:
                    embed.add_field(name="Entity Type", value=app_data.entity_type, inline=True)
                if app_data.entity_name:
                    embed.add_field(name="Name", value=app_data.entity_name, inline=True)
                if app_data.callsign:
                    embed.add_field(name="Callsign", value=app_data.callsign, inline=True)

                address = f"ATTN: {app_data.attention}\n" if app_data.attention else ""
                address += f"{app_data.street_address}\n" if app_data.street_address else ""
                address += f"{app_data.po_box}\n" if app_data.po_box else ""
                address += (f"{', '.join([app_data.locality, app_data.state.split('-')[0].strip()])}"
                            f" {app_data.postal_code}")
                if address:
                    embed.add_field(name="Address", value=address, inline=True)
                if app_data.county:
                    embed.add_field(name="County", value=app_data.county, inline=True)
                if app_data.maidenhead:
                    embed.add_field(name="Grid Square", value=app_data.maidenhead, inline=True)
                if app_data.uls_geo_region:
                    embed.add_field(name="Region", value=app_data.uls_geo_region, inline=True)
                if app_data.last_action_date:
                    embed.add_field(name="Last Action", value=f"{app_data.last_action_date:%Y-%m-%d}", inline=True)
                if app_data.receipt_date:
                    embed.add_field(name="Receipt Date", value=f"{app_data.receipt_date:%Y-%m-%d}", inline=True)
                if app_data.entered_timestamp:
                    embed.add_field(name="Entered Time", value=f"{app_data.entered_timestamp:%Y-%m-%d}", inline=True)
                if app_data.application_source:
                    embed.add_field(name="Application Source", value=app_data.application_source, inline=True)
                if app_data.application_purpose:
                    embed.add_field(name="Purpose", value=app_data.application_purpose, inline=True)
                if app_data.result:
                    embed.add_field(name="Result", value=app_data.result, inline=True)
                if app_data.fee_control_number:
                    embed.add_field(name="Fee Control Number", value=app_data.fee_control_number, inline=True)
                if app_data.payment_date:
                    embed.add_field(name="Payment Date", value=f"{app_data.payment_date:%Y-%m-%d}", inline=True)
                if app_data.operator_class:
                    embed.add_field(name="Operator Class", value=app_data.operator_class, inline=True)
                if app_data.operator_group:
                    embed.add_field(name="Operator Group", value=app_data.operator_group, inline=True)
                if app_data.uls_group:
                    embed.add_field(name="ULS Group", value=app_data.uls_group, inline=True)
                if app_data.vanity_type:
                    embed.add_field(name="Vanity Type", value=app_data.vanity_type, inline=True)
                if app_data.vanity_relationship:
                    embed.add_field(name="Vanity Relationship", value=app_data.vanity_relationship, inline=True)
                if app_data.trustee_name and app_data.trustee_callsign:
                    embed.add_field(name="Trustee",
                                    value=f"{app_data.trustee_name} ({app_data.trustee_callsign})",
                                    inline=True)

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="frn", aliases=["f"], category=cmn.cat.lookup)
    async def _ae7q_frn(self, ctx: commands.Context, frn: str):
        """Looks up the history of an FRN on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            frn = frn.upper()

            frn_data = ae7qparser.get_frn(frn)

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q FRN History for {frn}"
            embed.url = frn_data.query_url
            embed.colour = cmn.colours.good
            embed.description = ""

            if not frn_data.frn_history:
                embed.colour = cmn.colours.bad
                embed.description += f"\nNo records found for `{frn}`"
            else:
                # add the first three rows of the FRN history to the embed
                for row in frn_data.frn_history[0:3]:
                    header = f"**{row.callsign}** ({row.applicant_type})"
                    body = (f"Name: *{row.entity_name}*\n"
                            f"Region: *{row.region_state}*\n"
                            f"Operator Class: *{row.operator_class}*\n"
                            f"Status: *{row.license_status}*\n")
                    if row.grant_date:
                        body += f"Granted: *{row.grant_date:%Y-%m-%d}*\n"
                    if row.effective_date:
                        body += f"Effective: *{row.effective_date:%Y-%m-%d}*\n"
                    if row.cancel_date:
                        body += f"Cancelled: *{row.cancel_date:%Y-%m-%d}*\n"
                    if row.expire_date:
                        body += f"Expires: *{row.expire_date:%Y-%m-%d}*\n"
                    embed.add_field(name=header, value=body, inline=False)

                if len(frn_data.frn_history) > 3:
                    embed.description += (f"\nRecords 1 to 3 of {len(frn_data.frn_history)}. "
                                          f"See [ae7q.com]({frn_data.query_url}) for more...")

            await ctx.send(embed=embed)

    @_ae7q_lookup.command(name="licensee", aliases=["l"], category=cmn.cat.lookup)
    async def _ae7q_licensee(self, ctx: commands.Context, licensee_id: str):
        """Looks up the history of a licensee ID on [ae7q.com](http://ae7q.com/)."""
        with ctx.typing():
            licensee_id = licensee_id.upper()

            lid_data = ae7qparser.get_licensee_id(licensee_id)

            embed = cmn.embed_factory(ctx)
            embed.title = f"AE7Q History for Licensee {licensee_id}"
            embed.url = lid_data.query_url
            embed.colour = cmn.colours.good
            embed.description = ""

            if not lid_data.licensee_id_history:
                embed.colour = cmn.colours.bad
                embed.description += f"\nNo records found for `{licensee_id}`"
            else:
                # add the first three rows of the FRN history to the embed
                for row in lid_data.licensee_id_history[0:3]:
                    header = f"**{row.callsign}** ({row.applicant_type})"
                    body = (f"Name: *{row.entity_name}*\n"
                            f"Region: *{row.region_state}*\n"
                            f"Operator Class: *{row.operator_class}*\n"
                            f"Status: *{row.license_status}*\n")
                    if row.grant_date:
                        body += f"Granted: *{row.grant_date:%Y-%m-%d}*\n"
                    if row.effective_date:
                        body += f"Effective: *{row.effective_date:%Y-%m-%d}*\n"
                    if row.cancel_date:
                        body += f"Cancelled: *{row.cancel_date:%Y-%m-%d}*\n"
                    if row.expire_date:
                        body += f"Expires: *{row.expire_date:%Y-%m-%d}*\n"

                    embed.add_field(name=header, value=body, inline=False)

                if len(lid_data.licensee_id_history) > 3:
                    embed.description += (f"\nRecords 1 to 3 of {len(lid_data.licensee_id_history)}. "
                                          f"See [ae7q.com]({lid_data.query_url}) for more...")

            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(AE7QCog(bot))
