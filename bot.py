# bot/bot.py

import discord
from discord.ext import commands
import os

# Configuração de intents e prefixo
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de cogs
cogs = [
    "economy", "missions", "pvp", "pets", "events", "ranking",
    "alliance", "properties", "crafting", "seasons", "holidays",
    "reputation", "skills", "marketplace", "survival", "energy",
    "relationships", "cooking", "tournaments", "titles", "settings",
    "transaction_logs", "help", "weather", "investment"
]

# Carregar cada cog
for cog in cogs:
    try:
        bot.load_extension(f"cogs.{cog}")
        print(f"Cog {cog} carregado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar o cog {cog}: {e}")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Executar o bot
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
