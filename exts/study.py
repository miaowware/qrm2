"""
Study extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""

import random
import json
from datetime import datetime

import aiohttp

import discord.ext.commands as commands

import common as cmn


class StudyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastq = dict()
        self.source = 'Data courtesy of [HamStudy.org](https://hamstudy.org/)'
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.command(name="hamstudy", aliases=['rq', 'randomquestion', 'randomq'], category=cmn.cat.study)
    async def _random_question(self, ctx: commands.Context, country: str = '', level: str = ''):
        '''Gets a random question from [HamStudy's](https://hamstudy.org) question pools.'''
        with ctx.typing():
            embed = cmn.embed_factory(ctx)

            country = country.lower()
            level = level.lower()

            pool_names = {'us': {'technician': 'E2',
                                 'tech': 'E2',
                                 't': 'E2',
                                 'general': 'E3',
                                 'gen': 'E3',
                                 'g': 'E3',
                                 'extra': 'E4',
                                 'e': 'E4'},
                          'ca': {'basic': 'CA_B',
                                 'b': 'CA_B',
                                 'advanced': 'CA_A',
                                 'adv': 'CA_A',
                                 'a': 'CA_A',
                                 'basic_fr': 'CA_FB',
                                 'b_fr': 'CA_FB',
                                 'base': 'CA_FB',
                                 'advanced_fr': 'CA_FS',
                                 'adv_fr': 'CA_FS',
                                 'a_fr': 'CA_FS',
                                 'supérieure': 'CA_FS',
                                 'superieure': 'CA_FS',
                                 's': 'CA_FS'},
                          'us_c': {'c1': 'C1',
                                   'comm1': 'C1',
                                   'c3': 'C3',
                                   'comm3': 'C3',
                                   'c6': 'C6',
                                   'comm6': 'C6',
                                   'c7': 'C7',
                                   'comm7': 'C7',
                                   'c7r': 'C7R',
                                   'comm7r': 'C7R',
                                   'c8': 'C8',
                                   'comm8': 'C8',
                                   'c9': 'C9',
                                   'comm9': 'C9'}}

            if country in pool_names.keys():
                if level in pool_names[country].keys():
                    pool_name = pool_names[country][level]

                elif level in ("random", "r"):
                    # select a random level in that country
                    pool_name = random.choice(list(pool_names[country].values()))

                else:
                    # show list of possible pools
                    embed.title = "Pool Not Found!"
                    embed.description = "Possible arguments are:"
                    embed.colour = cmn.colours.bad
                    for cty in pool_names:
                        levels = '`, `'.join(pool_names[cty].keys())
                        embed.add_field(name=f"**Country: `{cty}`**", value=f"Levels: `{levels}`", inline=False)
                    await ctx.send(embed=embed)
                    return

            elif country in ("random", "r"):
                # select a random country and level
                country = random.choice(list(pool_names.keys()))
                pool_name = random.choice(list(pool_names[country].values()))

            else:
                # show list of possible pools
                embed.title = "Pool Not Found!"
                embed.description = "Possible arguments are:"
                embed.colour = cmn.colours.bad
                for cty in pool_names:
                    levels = '`, `'.join(pool_names[cty].keys())
                    embed.add_field(name=f"**Country: `{cty}`**", value=f"Levels: `{levels}`", inline=False)
                await ctx.send(embed=embed)
                return

            pools = await self.hamstudy_get_pools()

            pool_matches = [p for p in pools.keys() if p.startswith(pool_name)]

            if len(pool_matches) > 0:
                if len(pool_matches) == 1:
                    pool = pool_matches[0]
                else:
                    # look at valid_from and expires dates to find the correct one
                    for p in pool_matches:
                        valid_from = datetime.fromisoformat(pools[p]["valid_from"][:-1] + "+00:00")
                        expires = datetime.fromisoformat(pools[p]["expires"][:-1] + "+00:00")

                        if valid_from < datetime.utcnow() < expires:
                            pool = p
                            break
            else:
                # show list of possible pools
                embed.title = "Pool Not Found!"
                embed.description = "Possible arguments are:"
                embed.colour = cmn.colours.bad
                for cty in pool_names:
                    levels = '`, `'.join(pool_names[cty].keys())
                    embed.add_field(name=f"**Country: `{cty}`**", value=f"Levels: `{levels}`", inline=False)
                await ctx.send(embed=embed)
                return


            async with self.session.get(f'https://hamstudy.org/pools/{pool}') as resp:
                if resp.status != 200:
                    embed.title = 'Error in HamStudy command'
                    embed.description = 'Could not load questions'
                    embed.colour = cmn.colours.bad
                    await ctx.send(embed=embed)
                    return
                pool = json.loads(await resp.read())['pool']

            # Select a question
            pool_section = random.choice(pool)['sections']
            pool_questions = random.choice(pool_section)['questions']
            question = random.choice(pool_questions)

            embed.title = question['id']
            embed.description = self.source
            embed.colour = cmn.colours.good
            embed.add_field(name='Question:', value=question['text'], inline=False)
            embed.add_field(name='Answers:', value='**A:** ' + question['answers']['A']
                            + '\n**B:** ' + question['answers']['B']
                            + '\n**C:** ' + question['answers']['C']
                            + '\n**D:** ' + question['answers']['D'], inline=False)
            embed.add_field(name='Answer:', value='Type _?rqa_ for answer', inline=False)
            if 'image' in question:
                image_url = f'https://hamstudy.org/_1330011/images/{pool.split("_",1)[1]}/{question["image"]}'
                embed.set_image(url=image_url)
            self.lastq[ctx.message.channel.id] = (question['id'], question['answer'])
        await ctx.send(embed=embed)

    @commands.command(name="hamstudyanswer", aliases=['rqa', 'randomquestionanswer', 'randomqa', 'hamstudya'], category=cmn.cat.study)
    async def _q_answer(self, ctx: commands.Context, answer: str = None):
        '''Returns the answer to question last asked (Optional argument: your answer).'''
        with ctx.typing():
            correct_ans = self.lastq[ctx.message.channel.id][1]
            q_num = self.lastq[ctx.message.channel.id][0]
            embed = cmn.embed_factory(ctx)
            if answer is not None:
                answer = answer.upper()
                if answer == correct_ans:
                    result = f'Correct! The answer to {q_num} was **{correct_ans}**.'
                    embed.title = f'{q_num} Answer'
                    embed.description = f'{self.source}\n\n{result}'
                    embed.colour = cmn.colours.good
                else:
                    result = f'Incorrect. The answer to {q_num} was **{correct_ans}**, not **{answer}**.'
                    embed.title = f'{q_num} Answer'
                    embed.description = f'{self.source}\n\n{result}'
                    embed.colour = cmn.colours.bad
            else:
                result = f'The correct answer to {q_num} was **{correct_ans}**.'
                embed.title = f'{q_num} Answer'
                embed.description = f'{self.source}\n\n{result}'
                embed.colour = cmn.colours.neutral
        await ctx.send(embed=embed)

    async def hamstudy_get_pools(self):
        async with self.session.get('https://hamstudy.org/pools/') as resp:
            if resp.status != 200:
                raise ConnectionError
            else:
                pools_dict = json.loads(await resp.read())

        pools_list = []
        for l in pools_dict.values():
            pools_list += l

        pools = {p["id"]: p for p in pools_list}

        return pools


def setup(bot: commands.Bot):
    bot.add_cog(StudyCog(bot))
