# bot/cogs/titles.py

import discord
from discord.ext import commands

class Titles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def adicionar_titulo(self, user_id, titulo):
        await self.bot.db.execute(
            "UPDATE jogadores SET titulo = $1 WHERE user_id = $2",
            titulo, user_id
        )

    @commands.command()
    async def meus_titulos(self, ctx):
        titulos = await self.bot.db.fetch("SELECT titulo FROM jogadores WHERE user_id = $1", ctx.author.id)
        if not titulos:
            await ctx.send(f"{ctx.author.mention}, você ainda não possui títulos.")
        else:
            await ctx.send(f"{ctx.author.mention}, seus títulos: {', '.join([t['titulo'] for t in titulos])}")

    @commands.command()
    async def conquistar_titulo(self, ctx, titulo: str):
        # Adiciona lógica de validação e requisitos
        await self.adicionar_titulo(ctx.author.id, titulo)
        await ctx.send(f"{ctx.author.mention}, você conquistou o título: **{titulo}**!")

def setup(bot):
    bot.add_cog(Titles(bot))
