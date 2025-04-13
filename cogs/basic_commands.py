import discord
from discord.ext import commands
import random

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bonjour', help='Le bot vous salue')
    async def hello(self, ctx):
        """Dit bonjour à l'utilisateur"""
        messages = [
            f"Bonjour {ctx.author.mention} ! Comment ça va ?",
            f"Salut {ctx.author.mention} ! Ravi de te voir !",
            f"Hey {ctx.author.mention} ! Belle journée, n'est-ce pas ?"
        ]
        await ctx.send(random.choice(messages))

    @commands.command(name='info', help='Affiche des informations sur le serveur')
    async def server_info(self, ctx):
        """Affiche des informations sur le serveur Discord"""
        server = ctx.guild
        embed = discord.Embed(
            title=f"Informations sur {server.name}",
            description="Voici quelques informations sur ce serveur",
            color=discord.Color.blue()
        )
        
        # Ajout des champs dans l'embed
        embed.add_field(name="Créé le", value=server.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Propriétaire", value=server.owner.mention, inline=True)
        embed.add_field(name="Membres", value=server.member_count, inline=True)
        embed.add_field(name="Salons", value=len(server.channels), inline=True)
        
        # Ajout d'une image (logo du serveur) si disponible
        if server.icon:
            embed.set_thumbnail(url=server.icon.url)
        
        await ctx.send(embed=embed)

    @commands.command(name='dice', help='Lance un dé (nombre de faces par défaut: 6)')
    async def roll_dice(self, ctx, faces: int = 6):
        """Lance un dé avec le nombre de faces spécifié"""
        if faces < 2:
            await ctx.send("Un dé doit avoir au moins 2 faces !")
            return
            
        result = random.randint(1, faces)
        await ctx.send(f"🎲 Vous avez lancé un dé à {faces} faces et obtenu: **{result}**")

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
