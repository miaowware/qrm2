"""
Study cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import random
import json
from datetime import datetime

import discord
import discord.ext.commands as commands

import aiohttp

import global_settings as gs


class StudyCog(commands.Cog, name='HamStudy Commands'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastq = dict()

    @commands.command(name="rq", aliases=['randomq'], category=gs.cat.study)
    async def _random_question(self, ctx: commands.Context, level: str = None):
        '''Gets a random question from the Technician, General, and/or Extra question pools.'''
        tech_pool = 'E2_2018'
        gen_pool = 'E3_2019'
        extra_pool = 'E4_2016'

        with ctx.typing():
            selected_pool = None
            try:
                level = level.lower()
            except AttributeError:  # no level given (it's None)
                pass

            if level in ['t', 'technician', 'tech']:
                selected_pool = tech_pool

            if level in ['g', 'gen', 'general']:
                selected_pool = gen_pool

            if level in ['e', 'ae', 'extra']:
                selected_pool = extra_pool

            if (level is None) or (level == 'all'):  # no pool given or user wants all, so pick a random pool
                selected_pool = random.choice([tech_pool, gen_pool, extra_pool])
            if (level is not None) and (selected_pool is None):  # unrecognized pool given by user
                await ctx.send('The question pool you gave was unrecognized. ' +
                               'There are many ways to call up certain question pools - try ?rq t, g, or e. ' +
                               '(Note that only the US question pools are available).')
                return

            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://hamstudy.org/pools/{selected_pool}') as resp:
                    if resp.status != 200:
                        return await ctx.send('Could not load questions...')
                    pool = json.loads(await resp.read())['pool']

            # Select a question
            pool_section = random.choice(pool)['sections']
            pool_questions = random.choice(pool_section)['questions']
            question = random.choice(pool_questions)

            embed = discord.Embed(title=question['id'],
                                  description='Data courtesy of HamStudy.org',
                                  colour=gs.colours.good,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.author.name,
                             icon_url=str(ctx.author.avatar_url))
            embed = embed.add_field(name='Question:', value=question['text'], inline=False)
            embed = embed.add_field(name='Answers:', value='**A:** ' + question['answers']['A'] +
                                    '\n**B:** ' + question['answers']['B'] +
                                    '\n**C:** ' + question['answers']['C'] +
                                    '\n**D:** ' + question['answers']['D'],
                                    inline=False)
            embed = embed.add_field(name='Answer:', value='Type _?rqa_ for answer', inline=False)
            if 'image' in question:
                image_url = f'https://hamstudy.org/_1330011/images/{selected_pool.split("_",1)[1]}/{question["image"]}'
                embed = embed.set_image(url=image_url)
            self.lastq[ctx.message.channel.id] = (question['id'], question['answer'])
        await ctx.send(embed=embed)

    @commands.command(name="rqa", category=gs.cat.study)
    async def _q_answer(self, ctx: commands.Context, answer: str = None):
        '''Returns the answer to question last asked (Optional argument: your answer).'''
        with ctx.typing():
            correct_ans = self.lastq[ctx.message.channel.id][1]
            q_num = self.lastq[ctx.message.channel.id][0]
            if answer is not None:
                answer = answer.upper()
                if answer == correct_ans:
                    result = f'Correct! The answer to {q_num} was **{correct_ans}**.'
                    embed = discord.Embed(title=f'{q_num} Answer',
                                          description=f'Data courtesy of HamStudy.org\n\n{result}',
                                          colour=gs.colours.good,
                                          timestamp=datetime.utcnow())
                else:
                    result = f'Incorrect. The answer to {q_num} was **{correct_ans}**, not **{answer}**.'
                    embed = discord.Embed(title=f'{q_num} Answer',
                                          description=f'Data courtesy of HamStudy.org\n\n{result}',
                                          colour=gs.colours.bad,
                                          timestamp=datetime.utcnow())
            else:
                result = f'The correct answer to {q_num} was **{correct_ans}**.'
                embed = discord.Embed(title=f'{q_num} Answer',
                                      description=f'Data courtesy of HamStudy.org\n\n{result}',
                                      colour=gs.colours.neutral,
                                      timestamp=datetime.utcnow())

        embed.set_footer(text=ctx.author.name,
                         icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(StudyCog(bot))
