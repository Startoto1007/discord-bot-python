import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

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
        await bot.load_extension("cogs.basic_commands")
        synced = await bot.tree.sync()
        print(f"🔧 {len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des extensions : {e}")

# Lancement du bot
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ Le token Discord n'est pas défini. Vérifie la variable DISCORD_TOKEN sur Railway.")

bot.run(TOKEN)
