# bot/cogs/properties.py

import discord
from discord.ext import commands

class Properties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def comprar_casa(self, ctx, tipo: str):
        user_id = ctx.author.id
        preco = 500
        saldo = await self.bot.db.fetchval("SELECT saldo FROM jogadores WHERE user_id = $1", user_id)
        
        if saldo < preco:
            await ctx.send(f"{ctx.author.mention}, você não tem embers suficientes para comprar uma casa.")
        else:
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo - $1 WHERE user_id = $2", preco, user_id)
            await self.bot.db.execute("INSERT INTO propriedades (user_id, tipo, nivel) VALUES ($1, $2, $3)", user_id, tipo, 1)
            await ctx.send(f"{ctx.author.mention}, você comprou uma **{tipo}** por {preco} embers!")

    @commands.command()
    async def minha_casa(self, ctx):
        user_id = ctx.author.id
        propriedade = await self.bot.db.fetchrow("SELECT * FROM propriedades WHERE user_id = $1", user_id)

        if not propriedade:
            await ctx.send(f"{ctx.author.mention}, você ainda não possui uma casa.")
        else:
            await ctx.send(f"{ctx.author.mention}, sua casa é uma **{propriedade['tipo']}**, Nível: {propriedade['nivel']}.")

async def setup(bot):
    await bot.add_cog(Properties(bot))
