import os
import discord
from discord.ext import commands
import config
import asyncio

# Définition des intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Création du bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté au serveur Discord !')

    # Chargement des cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Module {filename} chargé avec succès.')

    # Sync commandes slash
    await bot.tree.sync()

    # Statut du bot
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Version 1.0.1"))

@bot.command(name='ping', help='Répond avec le temps de latence')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latence: {latency}ms')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande inconnue. Utilisez `!help` pour voir la liste des commandes.")
    else:
        print(f"Erreur : {error}")

if __name__ == "__main__":
    bot.run(config.TOKEN)
