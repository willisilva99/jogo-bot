# bot/cogs/investment.py

import discord
from discord.ext import commands, tasks
import random

class Investment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def investir(self, ctx, valor: int):
        user_id = ctx.author.id
        saldo = await self.bot.db.fetchval("SELECT saldo FROM jogadores WHERE user_id = $1", user_id)

        if saldo < valor:
            await ctx.send(f"{ctx.author.mention}, você não tem embers suficientes para investir essa quantia.")
            return

        await self.bot.db.execute("UPDATE jogadores SET saldo = saldo - $1 WHERE user_id = $2", valor, user_id)
        await self.bot.db.execute("INSERT INTO investimentos (user_id, valor_investido) VALUES ($1, $2)", user_id, valor)
        await ctx.send(f"{ctx.author.mention}, você investiu **{valor} embers**. Boa sorte!")

    @tasks.loop(hours=24)
    async def atualizar_investimentos(self):
        investimentos = await self.bot.db.fetch("SELECT id, user_id, valor_investido FROM investimentos")
        for investimento in investimentos:
            ganho = round(investimento['valor_investido'] * random.uniform(-0.1, 0.3))
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", ganho, investimento['user_id'])
            await self.bot.db.execute("DELETE FROM investimentos WHERE id = $1", investimento['id'])
            user = self.bot.get_user(investimento['user_id'])
            if user:
                await user.send(f"💼 Seu investimento resultou em **{'ganho' if ganho >= 0 else 'perda'} de {ganho} embers**!")

    @commands.Cog.listener()
    async def on_ready(self):
        self.atualizar_investimentos.start()

def setup(bot):
    bot.add_cog(Investment(bot))
