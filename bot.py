import discord
from discord.ext import commands, tasks
import os
import asyncpg
import asyncio
import random

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

# Mensagens de status aleatórias
status_messages = [
    "sobrevivendo ao apocalipse",
    "explorando novas bases",
    "caçando zumbis",
    "coletando recursos",
    "protegendo os sobreviventes",
    "negociando embers",
    "construindo alianças",
    "lutando contra hordas",
    "explorando o mapa",
    "realizando missões"
]

# Função para carregar os cogs
async def load_cogs():
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"Cog {cog} carregado com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar o cog {cog}: {e}")

# Tarefa para mudar o status do bot periodicamente
@tasks.loop(minutes=10)
async def change_status():
    new_status = random.choice(status_messages)
    await bot.change_presence(activity=discord.Game(new_status))

# Evento para notificar quando o bot está pronto
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    print("Bot está pronto e todos os cogs foram carregados.")
    change_status.start()  # Inicia a tarefa de status aleatório

# Função para configurar a conexão com o banco de dados
async def setup_database():
    try:
        bot.db = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"), min_size=1, max_size=10)
        print("Conexão com o banco de dados estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        await asyncio.sleep(5)  # Espera um pouco e tenta novamente
        await setup_database()

# Evento para capturar erros de comando e logar
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Ocorreu um erro: {error}")
    print(f"Erro detectado: {error}")

# Evento para capturar todas as mensagens (inclui o processamento de comandos)
@bot.event
async def on_message(message):
    # Ignora as mensagens do próprio bot
    if message.author == bot.user:
        return
    # Processa comandos nas mensagens
    await bot.process_commands(message)

# Função de setup principal
async def setup():
    await setup_database()  # Configura o banco de dados
    await load_cogs()       # Carrega os cogs
    await bot.start(os.getenv("TOKEN"))

# Iniciar o bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
