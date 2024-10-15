# bot/cogs/crafting.py

import discord
from discord.ext import commands
import random

class Crafting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coletar_material(self, ctx, material: str):
        user_id = ctx.author.id
        quantidade = random.randint(1, 5)
        await self.bot.db.execute("INSERT INTO crafting_materials (user_id, nome, quantidade) VALUES ($1, $2, $3) ON CONFLICT (user_id, nome) DO UPDATE SET quantidade = crafting_materials.quantidade + $3", user_id, material, quantidade)
        await ctx.send(f"{ctx.author.mention}, você coletou **{quantidade}** de **{material}**.")

    @commands.command()
    async def craft(self, ctx, item: str):
        user_id = ctx.author.id
        receitas = {
            "pocao": {"ervas": 3, "agua": 1}
        }

        if item not in receitas:
            await ctx.send("Receita inválida.")
            return

        materiais_requeridos = receitas[item]
        for material, quantidade in materiais_requeridos.items():
            atual = await self.bot.db.fetchval("SELECT quantidade FROM crafting_materials WHERE user_id = $1 AND nome = $2", user_id, material)
            if not atual or atual < quantidade:
                await ctx.send(f"{ctx.author.mention}, você não tem **{quantidade}** de **{material}** para craftar uma **{item}**.")
                return

        for material, quantidade in materiais_requeridos.items():
            await self.bot.db.execute("UPDATE crafting_materials SET quantidade = quantidade - $1 WHERE user_id = $2 AND nome = $3", quantidade, user_id, material)
        await ctx.send(f"{ctx.author.mention}, você craftou uma **{item}**!")

def setup(bot):
    bot.add_cog(Crafting(bot))
