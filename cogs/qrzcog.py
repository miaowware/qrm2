"""
QRZ cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""
from collections import OrderedDict

import discord
import discord.ext.commands as commands

from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup


class QRZCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="qrz", aliases=["call"])
    async def _qrz_lookup(self, ctx: commands.Context, call: str):
        '''Links to info about a callsign from QRZ.'''
        if self.gs.keys.qrz_user == '' or self.gs.keys.qrz_pass == '':
            await ctx.send(f'http://qrz.com/db/{call}')
            return
        try:
            # TODO: see if there's a key first (i.e. don't log in every time)
            # TODO: maybe make it a task to generate a key?
            key = await _qrz_login(self.gs.keys.qrz_user, self.gs.keys.qrz_pass)
        except ConnectionError as err:
            print(err)
        url = f'http://xmldata.qrz.com/xml/current/?s={key};callsign={call}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise ConnectionError(f'Unable to connect to QRZ (HTTP Error {resp.status})')
                resp_xml = await resp.text()

        xml_soup = BeautifulSoup(resp_xml, "xml")
        resp_data = {tag.name: tag.contents[0] for tag in xml_soup.select('QRZDatabase Callsign *')}
        resp_session = {tag.name: tag.contents[0] for tag in xml_soup.select('QRZDatabase Session *')}
        if 'Error' in resp_session:
            raise ValueError(resp_session['Error'])

        embed = discord.Embed(title=f"QRZ Data for {resp_data['call']}",
                              colour=self.gs.colours.good,
                              url=f'http://www.qrz.com/db/{resp_data["call"]}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        if 'image' in resp_data:
            embed.set_image(url=resp_data['image'])

        if 'name' in resp_data:
            if 'fname' in resp_data:
                name = resp_data['fname'] + ' ' + resp_data['name']
            else:
                name = resp_data['name']
        else:
            name = None
        if 'state' in resp_data:
            state = f', {resp_data["state"]}'
        else:
            state = ''
        address = resp_data.get('addr1', '') + '\n' + resp_data.get('addr2', '') + \
            state + ' ' + resp_data.get('zip', '')
        if 'eqsl' in resp_data:
            eqsl = 'Yes' if resp_data['eqsl'] == 1 else 'No'
        else:
            eqsl = 'Unknown'
        if 'mqsl' in resp_data:
            mqsl = 'Yes' if resp_data['mqsl'] == 1 else 'No'
        else:
            mqsl = 'Unknown'
        if 'lotw' in resp_data:
            lotw = 'Yes' if resp_data['lotw'] == 1 else 'No'
        else:
            lotw = 'Unknown'

        data = OrderedDict([('Name', name),
                            ('Country', resp_data.get('country', None)),
                            ('Address', address),
                            ('Grid Square', resp_data.get('grid', None)),
                            ('County', resp_data.get('county', None)),
                            ('CQ Zone', resp_data.get('cqzone', None)),
                            ('ITU Zone', resp_data.get('ituzone', None)),
                            ('IOTA Designator', resp_data.get('iota', None)),
                            ('Expires', resp_data.get('expdate', None)),
                            ('Aliases', resp_data.get('aliases', None)),
                            ('Previous Callsign', resp_data.get('p_call', None)),
                            ('License Class', resp_data.get('class', None)),
                            ('eQSL?', eqsl),
                            ('Paper QSL?', mqsl),
                            ('LotW?', lotw),
                            ('QSL Info', resp_data.get('qslmgr', None)),
                            ('CQ Zone', resp_data.get('cqzone', None)),
                            ('ITU Zone', resp_data.get('ituzone', None)),
                            ('IOTA Designator', resp_data.get('iota', None)),
                            ('Born', resp_data.get('born', None)),
                            ])
        for title, val in data.items():
            if val is not None:
                embed.add_field(name=title, value=val, inline=True)
        await ctx.send(embed=embed)


async def _qrz_login(user: str, passwd: str):
    url = f'http://xmldata.qrz.com/xml/current/?username={user};password={passwd};agent=qrmbot'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ConnectionError(f'Unable to connect to QRZ (HTTP Error {resp.status})')
            resp_xml = await resp.text()

    xml_soup = BeautifulSoup(resp_xml, "xml")
    resp_data = {tag.name: tag.contents[0] for tag in xml_soup.select('QRZDatabase Session *')}
    if 'Error' in resp_data:
        raise ConnectionError(resp_data['Error'])
    if resp_data['SubExp'] == 'non-subscriber':
        raise ConnectionError('Invalid QRZ Subscription')
    return resp_data['Key']


def setup(bot):
    bot.add_cog(QRZCog(bot))
