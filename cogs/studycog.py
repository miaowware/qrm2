"""
Study cog for qrm
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

import discord
import discord.ext.commands as commands

import random
import json
import aiohttp

class StudyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        self.lastq = dict()

    @commands.command(name="rq", aliases=['randomq'])
    async def _random_question(self, ctx, level: str = None):
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

            if (level is None) or (level == 'all'):  # no pool given or user wants all, so pick a random pool and use that
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

            embed = discord.Embed(title=question['id'], colour=self.gs.colours.good)
            embed = embed.add_field(name='Question:', value=question['text'], inline=False)
            embed = embed.add_field(name='Answers:', value=
                                    '**A:** ' + question['answers']['A'] +
                                    '\n**B:** ' + question['answers']['B'] +
                                    '\n**C:** ' + question['answers']['C'] +
                                    '\n**D:** ' + question['answers']['D'], inline=False)
            embed = embed.add_field(name='Answer:', value='Type _?rqa_ for answer', inline=False)
            if 'image' in question:
                image_url = f'https://hamstudy.org/_1330011/images/{selected_pool.split("_",1)[1]}/{question["image"]}'
                embed = embed.set_image(url=image_url)
            self.lastq[ctx.message.channel.id] = (question['id'], question['answer'])
        await ctx.send(embed=embed)

    @commands.command(name="rqa")
    async def _q_answer(self, ctx, ans: str = None):
        '''Returns the answer to question last asked (Optional argument: your answer).'''
        with ctx.typing():
            correct_ans = self.lastq[ctx.message.channel.id][1]
            q_num = self.lastq[ctx.message.channel.id][0]
            if ans is not None:
                ans = ans.upper()
                if ans == correct_ans:
                    result = f'Correct! The answer to {q_num} was **{correct_ans}**.'
                    embed = discord.Embed(title=f'{q_num} Answer', description=result, colour=self.gs.colours.good)
                else:
                    result = f'Incorrect. The answer to {q_num} was **{correct_ans}**, not **{ans}**.'
                    embed = discord.Embed(title=f'{q_num} Answer', description=result, colour=self.gs.colours.bad)
            else:
                result = f'The correct answer to {q_num} was **{correct_ans}**.'
                embed = discord.Embed(title=f'{q_num} Answer', description=result, colour=self.gs.colours.neutral)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(StudyCog(bot))
