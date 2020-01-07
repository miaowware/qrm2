"""
Study extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of discord-qrm2 and is released under the terms of the GNU
General Public License, version 2.
"""

import random
import json

import discord.ext.commands as commands

import common as cmn


class StudyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastq = dict()
        self.source = 'Data courtesy of [HamStudy.org](https://hamstudy.org/)'
        self.session = bot.qrm.session

    @commands.command(name="hamstudy", aliases=['rq', 'randomquestion', 'randomq'], category=cmn.cat.study)
    async def _random_question(self, ctx: commands.Context, level: str = None):
        '''Gets a random question from the Technician, General, and/or Extra question pools.'''
        tech_pool = 'E2_2018'
        gen_pool = 'E3_2019'
        extra_pool = 'E4_2016'

        embed = cmn.embed_factory(ctx)
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
                embed.title = 'Error in HamStudy command'
                embed.description = ('The question pool you gave was unrecognized. '
                                     'There are many ways to call up certain question pools - try ?rq t, g, or e. '
                                     '\n\nNote that currently only the US question pools are available.')
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
                return

            async with self.session.get(f'https://hamstudy.org/pools/{selected_pool}') as resp:
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
                image_url = f'https://hamstudy.org/_1330011/images/{selected_pool.split("_",1)[1]}/{question["image"]}'
                embed.set_image(url=image_url)
            self.lastq[ctx.message.channel.id] = (question['id'], question['answer'])
        await ctx.send(embed=embed)

    @commands.command(name="hamstudyanswer", aliases=['rqa', 'randomquestionanswer', 'randomqa', 'hamstudya'],
                      category=cmn.cat.study)
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


def setup(bot: commands.Bot):
    bot.add_cog(StudyCog(bot))
