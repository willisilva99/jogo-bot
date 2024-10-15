# bot/cogs/marketplace.py

import discord
from discord.ext import commands

class Marketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listar_leilao(self, ctx, item: str, preco: int):
        await self.bot.db.execute("INSERT INTO leiloes (item_nome, preco_inicial, preco_atual, dono_id) VALUES ($1, $2, $2, $3)", item, preco, ctx.author.id)
        await ctx.send(f"{ctx.author.mention} listou **{item}** para leilão por **{preco} embers**!")

    @commands.command()
    async def dar_lance(self, ctx, item_id: int, lance: int):
        leilao = await self.bot.db.fetchrow("SELECT * FROM leiloes WHERE id = $1", item_id)
        if not leilao:
            await ctx.send("Leilão não encontrado.")
            return
        if lance <= leilao['preco_atual']:
            await ctx.send("Seu lance precisa ser maior que o lance atual.")
            return
        await self.bot.db.execute("UPDATE leiloes SET preco_atual = $1, comprador_id = $2 WHERE id = $3", lance, ctx.author.id, item_id)
        await ctx.send(f"{ctx.author.mention} deu um lance de **{lance} embers** no item **{leilao['item_nome']}**!")

    @commands.command()
    async def listar_leiloes(self, ctx):
        leiloes = await self.bot.db.fetch("SELECT * FROM leiloes")
        if not leiloes:
            await ctx.send("Não há leilões ativos.")
            return
        leiloes_msg = "**Leilões Ativos:**\n"
        for leilao in leiloes:
            leiloes_msg += f"ID: {leilao['id']}, Item: {leilao['item_nome']}, Lance Atual: {leilao['preco_atual']} embers\n"
        await ctx.send(leiloes_msg)

async def setup(bot):
    await bot.add_cog(Marketplace(bot))

