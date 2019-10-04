"""
Info cog for qrm
---
"""

import discord
import discord.ext.commands as commands


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="info", aliases=["about"])
    async def _info(self, ctx):
        """Shows info about qrm."""
        embed = discord.Embed(title="About qrm", description=self.gs.info.description, colour=self.gs.colours.neutral)
        embed = embed.add_field(name="Authors", value=", ".join(self.gs.info.authors))
        embed = embed.add_field(name="Contributing", value=self.gs.info.contributing)
        embed = embed.add_field(name="License", value=self.gs.info.license)
        await ctx.send(embed=embed)

    @commands.command(name="restart")
    async def _restart_bot(self, ctx):
        """Restarts the bot."""
        if ctx.author.id in self.gs.opt.owners_uids:
            await ctx.message.add_reaction("✅")
            await self.bot.logout()
        else:
            try:
                await ctx.message.add_reaction("❌")
            except:
                return


def setup(bot):
    bot.add_cog(InfoCog(bot))
