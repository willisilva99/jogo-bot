# bot/cogs/weather.py

import discord
from discord.ext import commands, tasks
import random

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weather_status = "Ensolarado"
        self.change_weather.start()

    @tasks.loop(hours=1)
    async def change_weather(self):
        weather_conditions = ["Ensolarado", "Chuvoso", "Tempestuoso", "Nublado", "Nevando"]
        self.weather_status = random.choice(weather_conditions)
        channel = discord.utils.get(self.bot.get_all_channels(), name="geral")  # Alterar para o canal desejado
        if channel:
            await channel.send(f"🌤️ O clima mudou! Agora está {self.weather_status}.")

    @commands.command()
    async def clima(self, ctx):
        """Verifica o clima atual"""
        await ctx.send(f"O clima atual é: **{self.weather_status}**")

    @change_weather.before_loop
    async def before_change_weather(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Weather(bot))
