import discord
from discord.ext import commands
import os

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Initialisation du bot
intents = discord.Intents.default()
intents.members = True  # Nécessaire si tu veux interagir avec les membres du serveur

bot = commands.Bot(command_prefix="!", intents=intents)

# Charger les cogs (commandes) au démarrage du bot
@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    
    try:
        # Charger l'extension des commandes depuis le dossier /cogs/commands.py
        await bot.load_extension("cogs.commands")
    except Exception as e:
        print(f"Erreur lors du chargement des cogs : {e}")
    
    # Synchroniser les commandes slash avec Discord
    await bot.tree.sync()
    print("Commandes synchronisées.")

# Token de connexion
token = os.getenv("DISCORD_TOKEN")

# Démarrer le bot avec le token
bot.run(token)
