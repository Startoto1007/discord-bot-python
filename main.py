import discord
from discord.ext import commands
import os

# Créer l'instance du bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}!')

# Charger les cogs
@bot.event
async def on_ready():
    # Charger les extensions
    await bot.load_extension("cogs.basic_commands")
    await bot.load_extension("cogs.ticket")

# Récupérer le token depuis les variables d'environnement
TOKEN = os.getenv("DISCORD_TOKEN")

# Démarrer le bot avec le token
bot.run(TOKEN)
