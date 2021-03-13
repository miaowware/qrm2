"""
Study extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import random
import json
from datetime import datetime
import asyncio

import aiohttp

import discord.ext.commands as commands

import common as cmn
from resources import study


class StudyCog(commands.Cog):
    choices = {"A": cmn.emojis.a, "B": cmn.emojis.b, "C": cmn.emojis.c, "D": cmn.emojis.d, "E": cmn.emojis.e}
    choices_inv = {y: x for x, y in choices.items()}

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastq = dict()
        self.source = "Data courtesy of [HamStudy.org](https://hamstudy.org/)"
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.command(name="hamstudy", aliases=["rq", "randomquestion", "randomq"], category=cmn.cat.study)
    async def _random_question(self, ctx: commands.Context, country: str = "", level: str = "", element: str = ""):
        """Gets a random question from [HamStudy's](https://hamstudy.org) question pools."""
        with ctx.typing():
            embed = cmn.embed_factory(ctx)

            country = country.lower()
            level = level.lower()
            element = element.upper()

            if country in study.pool_names.keys():
                if level in study.pool_names[country].keys():
                    pool_name = study.pool_names[country][level]

                elif level in ("random", "r"):
                    # select a random level in that country
                    pool_name = random.choice(list(study.pool_names[country].values()))

                else:
                    # show list of possible pools
                    embed.title = "Pool Not Found!"
                    embed.description = "Possible arguments are:"
                    embed.colour = cmn.colours.bad
                    for cty in study.pool_names:
                        levels = "`, `".join(study.pool_names[cty].keys())
                        embed.add_field(name=f"**Country: `{cty}` {study.pool_emojis[cty]}**",
                                        value=f"Levels: `{levels}`", inline=False)
                    embed.add_field(name="**Random**", value="To select a random pool or country, use `random` or `r`")
                    await ctx.send(embed=embed)
                    return

            elif country in ("random", "r"):
                # select a random country and level
                country = random.choice(list(study.pool_names.keys()))
                pool_name = random.choice(list(study.pool_names[country].values()))

            else:
                # show list of possible pools
                embed.title = "Pool Not Found!"
                embed.description = "Possible arguments are:"
                embed.colour = cmn.colours.bad
                for cty in study.pool_names:
                    levels = "`, `".join(study.pool_names[cty].keys())
                    embed.add_field(name=f"**Country: `{cty}` {study.pool_emojis[cty]}**",
                                    value=f"Levels: `{levels}`", inline=False)
                embed.add_field(name="**Random**", value="To select a random pool or country, use `random` or `r`")
                await ctx.send(embed=embed)
                return

            pools = await self.hamstudy_get_pools()

            pool_matches = [p for p in pools.keys() if "_".join(p.split("_")[:-1]) == pool_name]

            if len(pool_matches) > 0:
                if len(pool_matches) == 1:
                    pool = pool_matches[0]
                else:
                    # look at valid_from and expires dates to find the correct one
                    for p in pool_matches:
                        valid_from = datetime.fromisoformat(pools[p]["valid_from"][:-1])
                        expires = datetime.fromisoformat(pools[p]["expires"][:-1])

                        if valid_from < datetime.utcnow() < expires:
                            pool = p
                            break
            else:
                # show list of possible pools
                embed.title = "Pool Not Found!"
                embed.description = "Possible arguments are:"
                embed.colour = cmn.colours.bad
                for cty in study.pool_names:
                    levels = "`, `".join(study.pool_names[cty].keys())
                    embed.add_field(name=f"**Country: `{cty}` {study.pool_emojis[cty]}**",
                                    value=f"Levels: `{levels}`", inline=False)
                embed.add_field(name="**Random**", value="To select a random pool or country, use `random` or `r`")
                await ctx.send(embed=embed)
                return

            pool_meta = pools[pool]

            async with self.session.get(f"https://hamstudy.org/pools/{pool}") as resp:
                if resp.status != 200:
                    raise cmn.BotHTTPError(resp)
                pool = json.loads(await resp.read())["pool"]

            # Select a question
            if element:
                els = [el["id"] for el in pool]
                if element in els:
                    pool_section = pool[els.index(element)]["sections"]
                else:
                    embed.title = "Element Not Found!"
                    embed.description = f"Possible Elements for Country `{country}` and Level `{level}` are:"
                    embed.colour = cmn.colours.bad
                    embed.description += "\n\n" + "`" + "`, `".join(els) + "`"
                    await ctx.send(embed=embed)
                    return
            else:
                pool_section = random.choice(pool)["sections"]
            pool_questions = random.choice(pool_section)["questions"]
            question = random.choice(pool_questions)
            answers = question['answers']
            answers_str = ""
            answers_str_bolded = ""
            for letter, ans in answers.items():
                answers_str += f"{self.choices[letter]} {ans}\n"
                if letter == question["answer"]:
                    answers_str_bolded += f"{self.choices[letter]} **{ans}**\n"
                else:
                    answers_str_bolded += f"{self.choices[letter]} {ans}\n"

            embed.title = f"{study.pool_emojis[country]} {pool_meta['class']} {question['id']}"
            embed.description = self.source
            embed.add_field(name="Question", value=question["text"], inline=False)
            embed.add_field(name="Answers", value=answers_str, inline=False)
            embed.add_field(name="To Answer",
                            value=("Answer with reactions below. If not answered within 5 minutes,"
                                   " the answer will be revealed."),
                            inline=False)
            if "image" in question:
                image_url = f"https://hamstudy.org/images/{pool_meta['year']}/{question['image']}"
                embed.set_image(url=image_url)

        q_msg = await ctx.send(embed=embed)

        for i in range(len(answers)):
            await cmn.add_react(q_msg, list(self.choices.values())[i])
        await cmn.add_react(q_msg, cmn.emojis.question)

        def check(reaction, user):
            return (user.id != self.bot.user.id
                    and reaction.message.id == q_msg.id
                    and (str(reaction.emoji) in self.choices.values() or str(reaction.emoji) == cmn.emojis.question))

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=300.0, check=check)
        except asyncio.TimeoutError:
            embed.set_field_at(1, name="Answers", value=answers_str_bolded, inline=False)
            embed.set_field_at(2, name="Answer",
                               value=(f"{cmn.emojis.clock} "
                                      f"**Timed out!** The correct answer was {self.choices[question['answer']]}"))
            embed.colour = cmn.colours.timeout
            await q_msg.edit(embed=embed)
        else:
            if str(reaction.emoji) == cmn.emojis.question:
                embed.set_field_at(1, name="Answers", value=answers_str_bolded, inline=False)
                embed.set_field_at(2, name="Answer",
                                   value=f"The correct answer was {self.choices[question['answer']]}", inline=False)
                embed.add_field(name="Answer Requested By", value=str(user), inline=False)
                embed.colour = cmn.colours.timeout
                await q_msg.edit(embed=embed)
            else:
                answers_str_checked = ""
                chosen_ans = self.choices_inv[str(reaction.emoji)]
                for letter, ans in answers.items():
                    answers_str_checked += f"{self.choices[letter]}"
                    if letter == question["answer"] == chosen_ans:
                        answers_str_checked += f"{cmn.emojis.check_mark} **{ans}**\n"
                    elif letter == question["answer"]:
                        answers_str_checked += f" **{ans}**\n"
                    elif letter == chosen_ans:
                        answers_str_checked += f"{cmn.emojis.x} {ans}\n"
                    else:
                        answers_str_checked += f" {ans}\n"

                if self.choices[question["answer"]] == str(reaction.emoji):
                    embed.set_field_at(1, name="Answers", value=answers_str_checked, inline=False)
                    embed.set_field_at(2, name="Answer", value=(f"{cmn.emojis.check_mark} "
                                                                f"**Correct!** The answer was {reaction.emoji}"))
                    embed.add_field(name="Answered By", value=str(user), inline=False)
                    embed.colour = cmn.colours.good
                    await q_msg.edit(embed=embed)
                else:
                    embed.set_field_at(1, name="Answers", value=answers_str_checked, inline=False)
                    embed.set_field_at(2, name="Answer",
                                       value=(f"{cmn.emojis.x} **Incorrect!** The correct answer was "
                                              f"{self.choices[question['answer']]}, not {reaction.emoji}"))
                    embed.add_field(name="Answered By", value=str(user), inline=False)
                    embed.colour = cmn.colours.bad
                    await q_msg.edit(embed=embed)

    async def hamstudy_get_pools(self):
        async with self.session.get("https://hamstudy.org/pools/") as resp:
            if resp.status != 200:
                raise cmn.BotHTTPError(resp)
            else:
                pools_dict = json.loads(await resp.read())

        pools = dict()
        for ls in pools_dict.values():
            for pool in ls:
                pools[pool["id"]] = pool

        return pools


def setup(bot: commands.Bot):
    bot.add_cog(StudyCog(bot))
