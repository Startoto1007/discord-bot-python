import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        await bot.load_extension("cogs.ticket")
        await bot.load_extension("cogs.basic_commands")
        print("Extensions chargées avec succès.")
    except Exception as e:
        print(f"Erreur lors du chargement des extensions : {e}")

async def main():
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
