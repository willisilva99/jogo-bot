# bot/cogs/seasons.py

import discord
from discord.ext import commands, tasks

class Seasons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.season = "Primavera"  # Temporada inicial
        self.change_season.start()

    @tasks.loop(hours=168)  # Troca de temporada a cada semana (168 horas)
    async def change_season(self):
        seasons = ["Primavera", "Verão", "Outono", "Inverno"]
        current_index = seasons.index(self.season)
        self.season = seasons[(current_index + 1) % len(seasons)]
        channel = discord.utils.get(self.bot.get_all_channels(), name="geral")  # Alterar para o canal desejado
        if channel:
            await channel.send(f"🍃 A nova temporada começou! Bem-vindo à **{self.season}**!")

    @commands.command()
    async def temporada(self, ctx):
        """Mostra a temporada atual"""
        await ctx.send(f"A temporada atual é: **{self.season}**")

    @change_season.before_loop
    async def before_change_season(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Seasons(bot))
