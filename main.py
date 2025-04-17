import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    # Charger les cogs
    try:
        await bot.load_extension("cogs.moderation")  # Pour la modération
        await bot.load_extension("cogs.ticket")      # Pour les tickets
    except Exception as e:
        print(f"Erreur lors du chargement des cogs : {e}")
    await bot.tree.sync()  # Synchroniser les commandes slash
    
# Démarrage du bot avec le token
bot.run(DISCORD_TOKEN)
