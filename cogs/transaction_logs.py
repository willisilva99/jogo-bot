# bot/cogs/transaction_logs.py

import discord
from discord.ext import commands

class TransactionLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_transaction(self, user_id, acao, quantidade):
        await self.bot.db.execute(
            "INSERT INTO historico_acoes (user_id, acao, quantidade) VALUES ($1, $2, $3)", 
            user_id, acao, quantidade
        )

    @commands.command()
    async def ver_historico(self, ctx):
        historico = await self.bot.db.fetch("SELECT acao, quantidade, timestamp FROM historico_acoes WHERE user_id = $1 ORDER BY timestamp DESC LIMIT 10", ctx.author.id)
        if not historico:
            await ctx.send(f"{ctx.author.mention}, você não tem histórico de transações.")
            return
        msg = "**Seu Histórico de Transações**:\n"
        for registro in historico:
            msg += f"{registro['acao'].capitalize()}: {registro['quantidade']} embers em {registro['timestamp']}\n"
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(TransactionLogs(bot))
