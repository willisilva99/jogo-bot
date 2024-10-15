# bot/cogs/holidays.py

import discord
from discord.ext import commands, tasks
from datetime import datetime

class Holidays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feriados = {
            "natal": {"recompensa": 300},
            "halloween": {"recompensa": 250}
        }

    @commands.command()
    async def feriado(self, ctx, nome: str):
        nome = nome.lower()
        if nome not in self.feriados:
            await ctx.send("Feriado inválido. Feriados disponíveis: `natal`, `halloween`.")
            return

        recompensa = self.feriados[nome]["recompensa"]
        user_id = ctx.author.id
        await self.bot.db.execute("UPDATE jogadores SET saldo = saldo + $1 WHERE user_id = $2", recompensa, user_id)
        await ctx.send(f"{ctx.author.mention}, você participou do feriado **{nome.capitalize()}** e ganhou **{recompensa} embers**!")

    @tasks.loop(hours=24)
    async def verificar_feriados(self):
        hoje = datetime.utcnow().strftime("%d-%m")
        feriados_do_dia = {
            "25-12": "natal",
            "31-10": "halloween"
        }

        if hoje in feriados_do_dia:
            nome = feriados_do_dia[hoje]
            canal = self.bot.get_channel(YOUR_CHANNEL_ID)
            if canal:
                await canal.send(f"🎉 Hoje é **{nome.capitalize()}**! Use `!feriado {nome}` para participar e ganhar embers!")

    @commands.Cog.listener()
    async def on_ready(self):
        self.verificar_feriados.start()

def setup(bot):
    bot.add_cog(Holidays(bot))
