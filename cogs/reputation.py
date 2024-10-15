# bot/cogs/reputation.py

import discord
from discord.ext import commands

class Reputation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def upvote(self, ctx, membro: discord.Member):
        if membro == ctx.author:
            await ctx.send("Você não pode dar um upvote para si mesmo!")
            return
        
        await self.bot.db.execute("UPDATE jogadores SET reputacao = reputacao + 1 WHERE user_id = $1", membro.id)
        await ctx.send(f"{ctx.author.mention} deu um upvote para {membro.mention}!")

    @commands.command()
    async def downvote(self, ctx, membro: discord.Member):
        if membro == ctx.author:
            await ctx.send("Você não pode dar um downvote para si mesmo!")
            return

        await self.bot.db.execute("UPDATE jogadores SET reputacao = reputacao - 1 WHERE user_id = $1", membro.id)
        await ctx.send(f"{ctx.author.mention} deu um downvote para {membro.mention}!")

    @commands.command()
    async def reputacao(self, ctx, membro: discord.Member = None):
        membro = membro or ctx.author
        reputacao = await self.bot.db.fetchval("SELECT reputacao FROM jogadores WHERE user_id = $1", membro.id) or 0
        await ctx.send(f"{membro.display_name} tem **{reputacao}** pontos de reputação.")

def setup(bot):
    bot.add_cog(Reputation(bot))
