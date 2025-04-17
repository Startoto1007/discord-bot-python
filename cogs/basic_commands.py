import discord
from discord.ext import commands
import random

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bonjour', help='Le bot vous salue')
    async def hello(self, ctx):
        messages = [
            f"Bonjour {ctx.author.mention} ! Comment ça va ?",
            f"Salut {ctx.author.mention} ! Ravi de te voir !",
            f"Hey {ctx.author.mention} ! Belle journée, n'est-ce pas ?"
        ]
        await ctx.send(random.choice(messages))

    @commands.command(name='info', help='Affiche des informations sur le serveur')
    async def server_info(self, ctx):
        server = ctx.guild
        embed = discord.Embed(
            title=f"Informations sur {server.name}",
            description="Voici quelques informations sur ce serveur",
            color=discord.Color.blue()
        )
        embed.add_field(name="Créé le", value=server.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Propriétaire", value=server.owner.mention, inline=True)
        embed.add_field(name="Membres", value=server.member_count, inline=True)
        embed.add_field(name="Salons", value=len(server.channels), inline=True)
        if server.icon:
            embed.set_thumbnail(url=server.icon.url)
        await ctx.send(embed=embed)

    @commands.command(name='dice', help='Lance un dé (nombre de faces par défaut: 6)')
    async def roll_dice(self, ctx, faces: int = 6):
        if faces < 2:
            await ctx.send("Un dé doit avoir au moins 2 faces !")
            return
        result = random.randint(1, faces)
        await ctx.send(f"🎲 Vous avez lancé un dé à {faces} faces et obtenu: **{result}**")

    @commands.command(name='ping', help='Teste la réactivité du bot')
    async def ping(self, ctx):
        await ctx.send("🏓 Pong !")

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
