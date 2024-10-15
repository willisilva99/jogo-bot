# bot/cogs/economy.py

import discord
from discord.ext import commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def saldo(self, ctx):
        user_id = ctx.author.id
        saldo = await self.bot.db.fetchval("SELECT saldo FROM jogadores WHERE user_id = $1", user_id)
        saldo = saldo if saldo else 0
        await ctx.send(f"{ctx.author.mention}, você tem **{saldo} embers**.")

    @commands.command()
    async def depositar(self, ctx, quantidade: int):
        user_id = ctx.author.id
        saldo = await self.bot.db.fetchval("SELECT saldo FROM jogadores WHERE user_id = $1", user_id)
        saldo = saldo if saldo else 0

        if saldo < quantidade:
            await ctx.send(f"{ctx.author.mention}, você não tem embers suficientes para depositar.")
            return

        await self.bot.db.execute("UPDATE jogadores SET saldo = saldo - $1, banco = banco + $1 WHERE user_id = $2", quantidade, user_id)
        await ctx.send(f"{ctx.author.mention}, você depositou **{quantidade} embers** no banco.")

    @commands.command()
    async def sacar(self, ctx, quantidade: int):
        user_id = ctx.author.id
        banco = await self.bot.db.fetchval("SELECT banco FROM jogadores WHERE user_id = $1", user_id)
        banco = banco if banco else 0

        if banco < quantidade:
            await ctx.send(f"{ctx.author.mention}, você não tem embers suficientes no banco para sacar.")
            return

        await self.bot.db.execute("UPDATE jogadores SET banco = banco - $1, saldo = saldo + $1 WHERE user_id = $2", quantidade, user_id)
        await ctx.send(f"{ctx.author.mention}, você sacou **{quantidade} embers** do banco.")

    @commands.command()
    async def trabalhar(self, ctx):
        user_id = ctx.author.id
        recompensa = random.randint(50, 150)
        await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", recompensa, user_id)
        await ctx.send(f"{ctx.author.mention}, você trabalhou e ganhou **{recompensa} embers**!")

async def setup(bot):
    await bot.add_cog(Economy(bot))  # Aguarde o add_cog
