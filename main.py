import os
import discord
from discord.ext import commands
import config
import asyncio

# Définition des intents (permissions) du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Création du bot avec le préfixe '!' pour les commandes
bot = commands.Bot(command_prefix='!', intents=intents)

# Événement déclenché lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté au serveur Discord!')

    # Chargement des cogs (modules)
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Module {filename} chargé avec succès.')

    # Synchronisation des commandes slash
    await bot.tree.sync()

    # Définition du statut personnalisé du bot
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="Version 1.0.1"))

# Commande de ping simple directement dans le fichier principal
@bot.command(name='ping', help='Répond avec le temps de latence')
async def ping(ctx):
    """Commande pour vérifier la latence du bot"""
    latency = round(bot.latency * 1000)  # Conversion en ms
    await ctx.send(f'Pong! Latence: {latency}ms')

# Gestion des erreurs
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande inconnue. Utilisez `!help` pour voir la liste des commandes disponibles.")
    else:
        print(f"Une erreur est survenue: {error}")

# Lancement du bot
if __name__ == "__main__":
    bot.run(config.TOKEN)
