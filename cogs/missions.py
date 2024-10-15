# bot/cogs/missions.py

import discord
from discord.ext import commands

class Missions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.missoes = {
            "Trabalhar 5 vezes": {"recompensa": 100, "condicao": "trabalhar", "quantidade": 5}
        }

    @commands.command()
    async def missoes(self, ctx):
        missao_texto = "\n".join([f"{missao}: {detalhe['recompensa']} embers" for missao, detalhe in self.missoes.items()])
        await ctx.send(f"🗒️ **Missões Ativas**:\n{missao_texto}")

    @commands.command()
    async def completar_missao(self, ctx, missao: str):
        missao = missao.lower()
        user_id = ctx.author.id
        progresso = await self.bot.db.fetchval("SELECT COUNT(*) FROM historico_acoes WHERE user_id = $1 AND acao = $2", user_id, self.missoes[missao]["condicao"])
        
        if progresso >= self.missoes[missao]["quantidade"]:
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", self.missoes[missao]["recompensa"], user_id)
            await ctx.send(f"{ctx.author.mention}, você completou a missão **{missao}** e ganhou **{self.missoes[missao]['recompensa']} embers**!")
        else:
            await ctx.send(f"{ctx.author.mention}, você ainda não completou a missão **{missao}**.")
            
async def setup(bot):
    await bot.add_cog(Missions(bot))  # Use await

