# bot/cogs/cooking.py

import discord
from discord.ext import commands

class Cooking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cozinhar(self, ctx, receita: str):
        if receita.lower() == "sopa":
            ingredientes = {"ervas": 3, "agua": 1}
            await ctx.send(f"{ctx.author.mention}, você está cozinhando uma sopa com {ingredientes}!")
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + 50 WHERE user_id = $1", ctx.author.id)
            await ctx.send(f"{ctx.author.mention}, você cozinhou uma sopa e ganhou **50 embers**!")

async def setup(bot):
    await bot.add_cog(Cooking(bot))

