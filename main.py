import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis un fichier .env si présent

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        await bot.load_extension("cogs.ticket")
        synced = await bot.tree.sync()
        print(f"🔧 {len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"❌ Erreur lors du chargement de l'extension : {e}")

# Remplace ici par ta commande test si tu veux
@bot.command()
async def ping(ctx):
    await ctx.send("pong !")

# Récupération du token depuis la variable d'environnement DISCORD_TOKEN
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ Le token Discord n'est pas défini. Assure-toi que la variable DISCORD_TOKEN est bien configurée sur Railway.")

bot.run(TOKEN)
