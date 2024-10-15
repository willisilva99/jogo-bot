# bot/bot.py

import discord
from discord.ext import commands
import os
import asyncpg
import asyncio

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
    print("Bot está pronto e todos os cogs foram carregados.")

async def setup():
    # Configurar a conexão com o banco de dados
    bot.db = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    await bot.start(os.getenv("TOKEN"))

# Iniciar o bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
