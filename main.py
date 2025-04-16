import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Charger les cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')  # Charge les cogs automatiquement
                print(f"Cog {filename} chargé avec succès!")
            except Exception as e:
                print(f"Erreur lors du chargement du cog {filename}: {e}")

# Ne pas oublier de démarrer le bot
bot.run("VOTRE_TOKEN")
