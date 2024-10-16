import discord
from discord.ext import commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def saldo(self, ctx):
        user_id = ctx.author.id
        saldo = await self.bot.db.fetchval("SELECT saldo FROM jogadores WHERE user_id = $1", user_id)
        saldo = saldo if saldo is not None else 0  # Verifica se saldo é None
        await ctx.send(f"{ctx.author.mention}, você tem **{saldo} embers**.")

    @commands.command()
    async def saldo_banco(self, ctx):
        user_id = ctx.author.id
        banco = await self.bot.db.fetchval("SELECT banco FROM jogadores WHERE user_id = $1", user_id)
        banco = banco if banco is not None else 0  # Verifica se banco é None
        await ctx.send(f"{ctx.author.mention}, você tem **{banco} embers** no banco.")

    @commands.command()
    async def depositar(self, ctx, quantidade: int):
        user_id = ctx.author.id

        # Verifica se o usuário existe
        usuario_existe = await self.bot.db.fetchval("SELECT COUNT(*) FROM jogadores WHERE user_id = $1", user_id)
        if usuario_existe is None or usuario_existe == 0:
            await ctx.send(f"{ctx.author.mention}, você não tem uma conta registrada.")
            return

        saldo = await self.bot.db.fetchval("SELECT saldo FROM jogadores WHERE user_id = $1", user_id)
        saldo = saldo if saldo is not None else 0  # Verifica se saldo é None

        if saldo < quantidade:
            await ctx.send(f"{ctx.author.mention}, você não tem embers suficientes para depositar.")
            return

        # Atualiza o saldo e o banco
        await self.bot.db.execute("UPDATE jogadores SET saldo = saldo - $1, banco = banco + $1 WHERE user_id = $2", quantidade, user_id)
        await ctx.send(f"{ctx.author.mention}, você depositou **{quantidade} embers** no banco.")

    @commands.command()
    async def sacar(self, ctx, quantidade: int):
        user_id = ctx.author.id

        # Verifica se o usuário existe
        usuario_existe = await self.bot.db.fetchval("SELECT COUNT(*) FROM jogadores WHERE user_id = $1", user_id)
        if usuario_existe is None or usuario_existe == 0:
            await ctx.send(f"{ctx.author.mention}, você não tem uma conta registrada.")
            return

        banco = await self.bot.db.fetchval("SELECT banco FROM jogadores WHERE user_id = $1", user_id)
        banco = banco if banco is not None else 0  # Verifica se banco é None

        if banco < quantidade:
            await ctx.send(f"{ctx.author.mention}, você não tem embers suficientes no banco para sacar.")
            return

        # Atualiza o banco e o saldo
        await self.bot.db.execute("UPDATE jogadores SET banco = banco - $1, saldo = saldo + $1 WHERE user_id = $2", quantidade, user_id)
        await ctx.send(f"{ctx.author.mention}, você sacou **{quantidade} embers** do banco.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def trabalhar(self, ctx):
        user_id = ctx.author.id
        recompensa = random.randint(10, 30)

        # Verifica se o usuário já existe
        saldo_existente = await self.bot.db.fetchval("SELECT saldo FROM jogadores WHERE user_id = $1", user_id)
        
        if saldo_existente is None:
            # Insere um novo jogador se não existir
            await self.bot.db.execute("INSERT INTO jogadores (user_id, saldo, banco, energia, nivel) VALUES ($1, $2, $3, $4, $5)", user_id, recompensa, 0, 100, 1)
        else:
            await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", recompensa, user_id)
        
        await ctx.send(f"{ctx.author.mention}, você trabalhou e ganhou **{recompensa} embers**!")

    @trabalhar.error
    async def trabalhar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            tempo_restante = int(error.retry_after // 60)
            await ctx.send(f"{ctx.author.mention}, você já trabalhou recentemente. Tente novamente em **{tempo_restante} minutos**.")

async def setup(bot):
    await bot.add_cog(Economy(bot))  # Aguarde o add_cog
