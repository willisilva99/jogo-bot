# bot/cogs/alliance.py

import discord
from discord.ext import commands

class Alliance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alianças = {}

    @commands.command()
    async def criar_aliança(self, ctx, nome: str):
        user_id = ctx.author.id
        if nome in self.alianças:
            await ctx.send(f"A aliança **{nome}** já existe.")
        else:
            self.alianças[nome] = [user_id]
            await ctx.send(f"{ctx.author.mention} criou a aliança **{nome}**.")

    @commands.command()
    async def juntar_aliança(self, ctx, nome: str):
        user_id = ctx.author.id
        if nome not in self.alianças:
            await ctx.send(f"A aliança **{nome}** não existe.")
        else:
            self.alianças[nome].append(user_id)
            await ctx.send(f"{ctx.author.mention} se juntou à aliança **{nome}**.")

    @commands.command()
    async def listar_alianças(self, ctx):
        if not self.alianças:
            await ctx.send("Não há alianças criadas ainda.")
        else:
            mensagem = "🤝 **Alianças Existentes** 🤝\n"
            for nome, membros in self.alianças.items():
                membros_nomes = [self.bot.get_user(uid).display_name for uid in membros if self.bot.get_user(uid)]
                mensagem += f"**{nome}**: {', '.join(membros_nomes)}\n"
            await ctx.send(mensagem)

async def setup(bot):
    await bot.add_cog(Alliance(bot))

