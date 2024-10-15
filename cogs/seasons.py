# bot/cogs/seasons.py

import discord
from discord.ext import commands, tasks

class Seasons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_season = "Primavera"
        self.pass_enabled = False

    @commands.command()
    async def iniciar_temporada(self, ctx, temporada: str):
        if self.pass_enabled:
            await ctx.send("Já há uma temporada em andamento.")
            return

        self.current_season = temporada.capitalize()
        self.pass_enabled = True
        await ctx.send(f"🏆 **Temporada {self.current_season}** iniciada! Use `!pass` para obter o Passe de Temporada.")

    @commands.command()
    async def pass(self, ctx):
        if not self.pass_enabled:
            await ctx.send("Não há uma temporada em andamento.")
            return

        user_id = ctx.author.id
        recompensa = 200
        await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", recompensa, user_id)
        await ctx.send(f"{ctx.author.mention}, você comprou o Passe de Temporada e ganhou **{recompensa} embers**!")

    @tasks.loop(days=30)
    async def finalizar_temporada(self):
        if self.pass_enabled:
            await self.bot.get_channel(YOUR_CHANNEL_ID).send(f"🏁 **Temporada {self.current_season}** terminou!")
            self.pass_enabled = False

    @commands.Cog.listener()
    async def on_ready(self):
        self.finalizar_temporada.start()

def setup(bot):
    bot.add_cog(Seasons(bot))
