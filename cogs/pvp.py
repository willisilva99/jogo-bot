# bot/cogs/pvp.py

import discord
from discord.ext import commands
import random

class PvP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duelo(self, ctx, oponente: discord.Member):
        atacante = ctx.author
        defensor = oponente

        if atacante == defensor:
            await ctx.send("Você não pode duelar contra si mesmo!")
            return

        ataque_atacante = random.randint(50, 150)
        ataque_defensor = random.randint(50, 150)

        if ataque_atacante > ataque_defensor:
            vencedor = atacante
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + 50 WHERE user_id = $1", vencedor.id)
            await ctx.send(f"{vencedor.mention} venceu o duelo e ganhou **50 embers**!")
        else:
            vencedor = defensor
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + 50 WHERE user_id = $1", vencedor.id)
            await ctx.send(f"{vencedor.mention} venceu o duelo e ganhou **50 embers**!")

async def setup(bot):
    await bot.add_cog(PvP(bot))

