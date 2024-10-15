# bot/cogs/skills.py

import discord
from discord.ext import commands

class Skills(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.classes = {
            "Guerreiro": {"bonus": "força"},
            "Mago": {"bonus": "magia"},
            "Ladrão": {"bonus": "agilidade"}
        }

    @commands.command()
    async def escolher_classe(self, ctx, classe: str):
        classe = classe.capitalize()
        if classe not in self.classes:
            await ctx.send("Classe inválida. Escolha entre `Guerreiro`, `Mago` ou `Ladrão`.")
            return

        await self.bot.db.execute("UPDATE jogadores SET classe = $1 WHERE user_id = $2", classe, ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, você escolheu a classe **{classe}** com bônus em **{self.classes[classe]['bonus']}**!")

    @commands.command()
    async def minha_classe(self, ctx):
        classe = await self.bot.db.fetchval("SELECT classe FROM jogadores WHERE user_id = $1", ctx.author.id)
        if not classe:
            await ctx.send("Você ainda não escolheu uma classe. Use `!escolher_classe` para escolher uma.")
        else:
            await ctx.send(f"{ctx.author.mention}, sua classe é **{classe}**.")

async def setup(bot):
    await bot.add_cog(Skills(bot))
