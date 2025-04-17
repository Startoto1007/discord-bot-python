import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio

# ID du rôle OB
OB_ROLE_ID = 1339286435475230800

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticket", help="Créer un ticket d'assistance")
    async def create_ticket(self, ctx):
        # Créer un message d'accueil avec un bouton
        button = Button(label="Ouvrir un ticket", style=discord.ButtonStyle.green)
        view = View()
        view.add_item(button)

        async def button_callback(interaction: discord.Interaction):
            # Vérifie si la personne est un membre de l'OB
            if OB_ROLE_ID in [role.id for role in interaction.user.roles]:
                await self.create_ticket_channel(interaction)
            else:
                await interaction.response.send_message("Désolé, vous n'avez pas le rôle nécessaire.", ephemeral=True)

        button.callback = button_callback
        await ctx.send("Cliquez pour créer un ticket.", view=view)

    async def create_ticket_channel(self, interaction: discord.Interaction):
        # Créer un salon privé pour le ticket
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        ticket_channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True)
            }
        )

        # Message d'introduction dans le salon
        await ticket_channel.send(f"Ticket ouvert par {interaction.user.mention}. Que puis-je faire pour vous ?")

        # Notification pour l'équipe OB
        notification_channel = discord.utils.get(guild.text_channels, id=1339334513658167397)
        await notification_channel.send(f"Un nouveau ticket a été créé par {interaction.user.mention}.")

async def setup(bot):
    await bot.add_cog(Ticket(bot))
