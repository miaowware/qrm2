"""
QRZ cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""
from collections import OrderedDict
from datetime import datetime

import discord
from discord.ext import commands, tasks

import aiohttp
from bs4 import BeautifulSoup


class QRZCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        self.session = aiohttp.ClientSession()
        self._qrz_session_init.start()

    @commands.command(name="qrz", aliases=["call"])
    async def _qrz_lookup(self, ctx: commands.Context, call: str):
        if self.gs.keys.qrz_user == '' or self.gs.keys.qrz_pass == '':
            await ctx.send(f'http://qrz.com/db/{call}')
            return

        try:
            await qrz_test_session(self.key, self.session)
        except ConnectionError:
            await self.get_session()

        url = f'http://xmldata.qrz.com/xml/current/?s={self.key};callsign={call}'
        async with self.session.get(url) as resp:
            if resp.status != 200:
                raise ConnectionError(f'Unable to connect to QRZ (HTTP Error {resp.status})')
            resp_xml = await resp.text()

        xml_soup = BeautifulSoup(resp_xml, "xml")

        resp_data = {tag.name: tag.contents[0] for tag in xml_soup.select('QRZDatabase Callsign *')}
        resp_session = {tag.name: tag.contents[0] for tag in xml_soup.select('QRZDatabase Session *')}
        if 'Error' in resp_session:
            if 'Session Timeout' in resp_session['Error']:
                await self.get_session()
            raise ValueError(resp_session['Error'])

        embed = discord.Embed(title=f"QRZ Data for {resp_data['call']}",
                              colour=self.gs.colours.good,
                              url=f'http://www.qrz.com/db/{resp_data["call"]}',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        if 'image' in resp_data:
            embed.set_image(url=resp_data['image'])

        data = qrz_process_info(resp_data)

        for title, val in data.items():
            if val is not None:
                embed.add_field(name=title, value=val, inline=True)
        await ctx.send(embed=embed)

    async def get_session(self):
        """Session creation and caching."""
        self.key = await qrz_login(self.gs.keys.qrz_user, self.gs.keys.qrz_pass, self.session)
        with open('data/qrz_session', 'w') as qrz_file:
            qrz_file.write(self.key)

    @tasks.loop(count=1)
    async def _qrz_session_init(self):
        """Helper task to allow obtaining a session at cog instantiation."""
        try:
            with open('data/qrz_session') as qrz_file:
                self.key = qrz_file.readline().strip()
            await qrz_test_session(self.key, self.session)
        except (FileNotFoundError, ConnectionError):
            await self.get_session()


async def qrz_login(user: str, passwd: str, session: aiohttp.ClientSession):
    url = f'http://xmldata.qrz.com/xml/current/?username={user};password={passwd};agent=qrmbot'
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


async def qrz_test_session(key: str, session: aiohttp.ClientSession):
    url = f'http://xmldata.qrz.com/xml/current/?s={key}'
    async with session.get(url) as resp:
        if resp.status != 200:
            raise ConnectionError(f'Unable to connect to QRZ (HTTP Error {resp.status})')
        resp_xml = await resp.text()

    xml_soup = BeautifulSoup(resp_xml, "xml")

    resp_session = {tag.name: tag.contents[0] for tag in xml_soup.select('QRZDatabase Session *')}
    if 'Error' in resp_session:
        raise ConnectionError(resp_session['Error'])


def qrz_process_info(data: dict):
    if 'name' in data:
        if 'fname' in data:
            name = data['fname'] + ' ' + data['name']
        else:
            name = data['name']
    else:
        name = None
    if 'state' in data:
        state = f', {data["state"]}'
    else:
        state = ''
    address = data.get('addr1', '') + '\n' + data.get('addr2', '') + \
        state + ' ' + data.get('zip', '')
    if 'eqsl' in data:
        eqsl = 'Yes' if data['eqsl'] == 1 else 'No'
    else:
        eqsl = 'Unknown'
    if 'mqsl' in data:
        mqsl = 'Yes' if data['mqsl'] == 1 else 'No'
    else:
        mqsl = 'Unknown'
    if 'lotw' in data:
        lotw = 'Yes' if data['lotw'] == 1 else 'No'
    else:
        lotw = 'Unknown'

    return OrderedDict([('Name', name),
                        ('Country', data.get('country', None)),
                        ('Address', address),
                        ('Grid Square', data.get('grid', None)),
                        ('County', data.get('county', None)),
                        ('CQ Zone', data.get('cqzone', None)),
                        ('ITU Zone', data.get('ituzone', None)),
                        ('IOTA Designator', data.get('iota', None)),
                        ('Expires', data.get('expdate', None)),
                        ('Aliases', data.get('aliases', None)),
                        ('Previous Callsign', data.get('p_call', None)),
                        ('License Class', data.get('class', None)),
                        ('eQSL?', eqsl),
                        ('Paper QSL?', mqsl),
                        ('LotW?', lotw),
                        ('QSL Info', data.get('qslmgr', None)),
                        ('CQ Zone', data.get('cqzone', None)),
                        ('ITU Zone', data.get('ituzone', None)),
                        ('IOTA Designator', data.get('iota', None)),
                        ('Born', data.get('born', None)),
                        ])


def setup(bot):
    bot.add_cog(QRZCog(bot))
