import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration du bot
TOKEN = os.getenv('DISCORD_TOKEN')
