# bot/cogs/help.py

import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ajuda(self, ctx, comando: str = None):
        if comando is None:
            msg = (
                "**Comandos Principais**\n"
                "`!ajuda [comando]` - Mostra detalhes sobre um comando.\n"
                "`!saldo` - Ver seu saldo de embers.\n"
                "`!trabalhar` - Trabalhar para ganhar embers.\n"
                "`!ranking` - Ver os rankings de embers e níveis.\n"
                "`!investir` - Investir uma quantia de embers.\n"
                "`!duelo` - Desafiar outro jogador em um duelo.\n"
                "Use `!ajuda [comando]` para ver detalhes de um comando específico."
            )
        else:
            detalhes = {
                "saldo": "`!saldo` - Mostra seu saldo atual de embers.",
                "trabalhar": "`!trabalhar` - Trabalha para ganhar embers. Cooldown de 10 minutos.",
                "ranking": "`!ranking [saldo/nivel]` - Exibe o ranking de embers ou de nível.",
                "investir": "`!investir [quantia]` - Investe embers e pode gerar ganhos ou perdas.",
                "duelo": "`!duelo @jogador` - Inicia um duelo com outro jogador."
            }
            msg = detalhes.get(comando.lower(), "Comando não encontrado.")
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Help(bot))
