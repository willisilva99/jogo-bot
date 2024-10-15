# bot/cogs/survival.py

import discord
from discord.ext import commands, tasks
import random

class Survival(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sobrevivencia_ativa = False

    @commands.command()
    async def iniciar_sobrevivencia(self, ctx):
        if self.sobrevivencia_ativa:
            await ctx.send("Um evento de sobrevivência já está em andamento!")
        else:
            self.sobrevivencia_ativa = True
            await ctx.send("🚨 Evento de Sobrevivência iniciado! Prepare-se para enfrentar ondas de inimigos!")

    @commands.command()
    async def atacar_horda(self, ctx):
        if not self.sobrevivencia_ativa:
            await ctx.send("Não há um evento de sobrevivência ativo.")
            return
        
        dano = random.randint(20, 100)
        await ctx.send(f"{ctx.author.mention} causou **{dano}** de dano na horda de inimigos!")

    @tasks.loop(minutes=5)
    async def terminar_sobrevivencia(self):
        if self.sobrevivencia_ativa:
            self.sobrevivencia_ativa = False
            await self.bot.get_channel(YOUR_CHANNEL_ID).send("🏁 O evento de sobrevivência terminou! Obrigado a todos que participaram.")

    @commands.Cog.listener()
    async def on_ready(self):
        self.terminar_sobrevivencia.start()

async def setup(bot):
    await bot.add_cog(Survival(bot))

