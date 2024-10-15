# bot/cogs/pets.py

import discord
from discord.ext import commands

class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pets = {}  # Dicionário para armazenar os pets dos usuários

    @commands.command()
    async def adotar(self, ctx, pet_name: str):
        """Permite que o jogador adote um pet"""
        user_id = ctx.author.id
        if user_id in self.pets:
            await ctx.send(f"{ctx.author.mention}, você já tem um pet chamado {self.pets[user_id]}!")
        else:
            self.pets[user_id] = pet_name
            await ctx.send(f"{ctx.author.mention} adotou um pet chamado **{pet_name}**!")

    @commands.command()
    async def meu_pet(self, ctx):
        """Exibe o pet atual do jogador"""
        user_id = ctx.author.id
        pet = self.pets.get(user_id)
        if pet:
            await ctx.send(f"{ctx.author.mention}, seu pet atual é **{pet}**.")
        else:
            await ctx.send(f"{ctx.author.mention}, você ainda não adotou um pet!")

    @commands.command()
    async def alimentar(self, ctx):
        """Alimenta o pet e aumenta sua lealdade"""
        user_id = ctx.author.id
        pet = self.pets.get(user_id)
        if pet:
            await ctx.send(f"{ctx.author.mention} alimentou **{pet}**! Ele está mais leal a você.")
        else:
            await ctx.send(f"{ctx.author.mention}, você precisa adotar um pet antes de alimentá-lo!")

async def setup(bot):
    await bot.add_cog(Pets(bot))
