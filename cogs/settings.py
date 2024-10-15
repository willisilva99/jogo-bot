# bot/cogs/settings.py

import discord
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def definir_notificacoes(self, ctx, opcao: str):
        opcao = opcao.lower()
        if opcao not in ["ativadas", "desativadas"]:
            await ctx.send("Use `!definir_notificacoes ativadas` ou `!definir_notificacoes desativadas`.")
            return
        await self.bot.db.execute("UPDATE jogadores SET notificacoes = $1 WHERE user_id = $2", opcao == "ativadas", ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, suas notificações de eventos foram **{opcao}**.")

    @commands.command()
    async def minhas_configuracoes(self, ctx):
        notificacoes = await self.bot.db.fetchval("SELECT notificacoes FROM jogadores WHERE user_id = $1", ctx.author.id)
        notificacoes_status = "ativadas" if notificacoes else "desativadas"
        await ctx.send(f"{ctx.author.mention}, suas notificações de eventos estão **{notificacoes_status}**.")

def setup(bot):
    bot.add_cog(Settings(bot))
