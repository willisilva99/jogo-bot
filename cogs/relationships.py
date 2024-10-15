# bot/cogs/relationships.py

import discord
from discord.ext import commands

class Relationships(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.casamentos = {}

    @commands.command()
    async def casar(self, ctx, parceiro: discord.Member):
        proponente = ctx.author
        if proponente.id in self.casamentos or parceiro.id in self.casamentos:
            await ctx.send("Um dos jogadores já está casado!")
            return

        def check(m):
            return m.author == parceiro and m.content.lower() in ["sim", "não"]

        await ctx.send(f"{parceiro.mention}, {proponente.mention} quer se casar com você! Responda com `sim` ou `não`.")
        try:
            resposta = await self.bot.wait_for("message", check=check, timeout=60)
            if resposta.content.lower() == "sim":
                self.casamentos[proponente.id] = parceiro.id
                self.casamentos[parceiro.id] = proponente.id
                await ctx.send(f"{proponente.mention} e {parceiro.mention} agora estão casados! 🎉")
            else:
                await ctx.send(f"{parceiro.mention} recusou o pedido de casamento.")
        except:
            await ctx.send(f"{parceiro.mention} não respondeu ao pedido de casamento.")

async def setup(bot):
    await bot.add_cog(Relationships(bot))

