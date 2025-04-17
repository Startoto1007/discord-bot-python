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
    try:
        # Charger les extensions
        await bot.load_extension("cogs.moderation")
        await bot.load_extension("cogs.ticket")
    except Exception as e:
        print(f"Erreur lors du chargement des cogs : {e}")

    # Synchroniser les commandes slash
    await bot.tree.sync()
    print("Commandes synchronisées.")
    
# Démarrage du bot avec le token
bot.run(DISCORD_TOKEN)
