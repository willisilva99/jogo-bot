# bot/cogs/ranking.py

import discord
from discord.ext import commands

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranking(self, ctx, tipo: str = "saldo"):
        if tipo == "saldo":
            jogadores = await self.bot.db.fetch("SELECT user_id, saldo FROM jogadores ORDER BY saldo DESC LIMIT 10")
            ranking_msg = "💰 **Ranking de Embers** 💰\n"
            for idx, jogador in enumerate(jogadores, 1):
                user = self.bot.get_user(jogador['user_id'])
                ranking_msg += f"{idx}. {user.display_name if user else 'Usuário Desconhecido'} - {jogador['saldo']} embers\n"
            await ctx.send(ranking_msg)
        elif tipo == "nivel":
            jogadores = await self.bot.db.fetch("SELECT user_id, nivel FROM jogadores ORDER BY nivel DESC LIMIT 10")
            ranking_msg = "🌟 **Ranking de Nível** 🌟\n"
            for idx, jogador in enumerate(jogadores, 1):
                user = self.bot.get_user(jogador['user_id'])
                ranking_msg += f"{idx}. {user.display_name if user else 'Usuário Desconhecido'} - Nível {jogador['nivel']}\n"
            await ctx.send(ranking_msg)
        else:
            await ctx.send("Tipo de ranking inválido. Use `!ranking saldo` ou `!ranking nivel`.")

def setup(bot):
    bot.add_cog(Ranking(bot))
