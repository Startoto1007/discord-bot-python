import discord
from discord.ext import commands
import asyncio
import os

# Chargement du token depuis un fichier config.py
from config import TOKEN  # Assure-toi que tu as un fichier config.py avec TOKEN = "ton_token"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Slash commands synchronisées ({len(synced)} commandes)")
    except Exception as e:
        print(f"Erreur de synchronisation des commandes : {e}")

# Chargement automatique des cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"🔄 Cog chargé : {filename}")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {filename} : {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
