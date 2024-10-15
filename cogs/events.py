# bot/cogs/events.py

import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import random

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.evento_ativo = False
        self.evento_hora_fim = None
        self.participantes = []

    @commands.command()
    async def evento(self, ctx):
        if not self.evento_ativo:
            self.evento_ativo = True
            self.evento_hora_fim = datetime.utcnow() + timedelta(minutes=10)
            self.participantes = []
            await ctx.send("🚨 Um evento começou! Use `!participar` para se juntar!")
        else:
            tempo_restante = (self.evento_hora_fim - datetime.utcnow()).seconds // 60
            await ctx.send(f"🚨 Evento em andamento! Faltam {tempo_restante} minutos.")

    @commands.command()
    async def participar(self, ctx):
        user_id = ctx.author.id
        if not self.evento_ativo:
            await ctx.send("Não há eventos ativos no momento.")
            return
        if user_id in self.participantes:
            await ctx.send(f"{ctx.author.mention}, você já está participando!")
        else:
            self.participantes.append(user_id)
            await ctx.send(f"{ctx.author.mention} se juntou ao evento!")

    @tasks.loop(seconds=10)
    async def verificar_evento(self):
        if self.evento_ativo and datetime.utcnow() > self.evento_hora_fim:
            self.evento_ativo = False
            self.evento_hora_fim = None
            for user_id in self.participantes:
                recompensa = random.randint(20, 100)
                await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", recompensa, user_id)
                user = self.bot.get_user(user_id)
                if user:
                    await user.send(f"🎉 O evento terminou! Você ganhou **{recompensa} embers**.")
            self.participantes = []

    @commands.Cog.listener()
    async def on_ready(self):
        self.verificar_evento.start()

def setup(bot):
    bot.add_cog(Events(bot))
