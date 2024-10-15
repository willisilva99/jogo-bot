# bot/cogs/energy.py

import discord
from discord.ext import commands, tasks

class Energy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def energia(self, ctx):
        energia = await self.bot.db.fetchval("SELECT energia FROM jogadores WHERE user_id = $1", ctx.author.id) or 100
        await ctx.send(f"{ctx.author.mention}, você tem **{energia}** pontos de energia.")

    @commands.command()
    async def restaurar_energia(self, ctx):
        await self.bot.db.execute("UPDATE jogadores SET energia = 100 WHERE user_id = $1", ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, sua energia foi restaurada para 100 pontos!")

    @tasks.loop(hours=1)
    async def regenerar_energia(self):
        await self.bot.db.execute("UPDATE jogadores SET energia = LEAST(energia + 10, 100)")

    @commands.Cog.listener()
    async def on_ready(self):
        self.regenerar_energia.start()

async def setup(bot):
    await bot.add_cog(Energy(bot))

