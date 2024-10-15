# bot/cogs/tournaments.py

import discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta

class Tournaments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.torneio_ativo = False
        self.jogadores = []

    @commands.command()
    async def entrar_torneio(self, ctx):
        if not self.torneio_ativo:
            await ctx.send("Nenhum torneio está ativo no momento.")
            return

        if ctx.author.id in self.jogadores:
            await ctx.send("Você já está inscrito no torneio!")
        else:
            self.jogadores.append(ctx.author.id)
            await ctx.send(f"{ctx.author.mention} entrou no torneio!")

    @commands.command()
    async def iniciar_torneio(self, ctx):
        if self.torneio_ativo:
            await ctx.send("Um torneio já está em andamento.")
            return

        self.torneio_ativo = True
        self.jogadores = []
        await ctx.send("🏆 Um novo torneio começou! Use `!entrar_torneio` para participar.")

    @tasks.loop(hours=1)
    async def terminar_torneio(self):
        if self.torneio_ativo and self.jogadores:
            vencedor_id = random.choice(self.jogadores)
            vencedor = self.bot.get_user(vencedor_id)
            premio = 500
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", premio, vencedor_id)
            await self.bot.get_channel(YOUR_CHANNEL_ID).send(f"🏆 Parabéns a {vencedor.mention} por vencer o torneio e ganhar **{premio} embers**!")
            self.torneio_ativo = False
            self.jogadores = []

    @commands.Cog.listener()
    async def on_ready(self):
        self.terminar_torneio.start()

def setup(bot):
    bot.add_cog(Tournaments(bot))
