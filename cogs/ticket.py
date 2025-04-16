# ticket.py
import discord
from discord.ext import commands
from discord import app_commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_message_id = None

    @app_commands.command(name="ticket", description="Commandes liées aux tickets")
    @app_commands.describe(salon="Salon où envoyer le menu de création de ticket")
    async def ticket_setup(self, interaction: discord.Interaction, salon: discord.TextChannel):
        if 1339286435475230800 not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("Tu n'as pas la permission d'utiliser cette commande.", ephemeral=True)

        menu = discord.ui.Select(
            placeholder="Choisis un type de ticket...",
            options=[
                discord.SelectOption(label="Signaler un problème dans le PW de l’OB Zelda", value="probleme_pw"),
                discord.SelectOption(label="Demander de l’aide sur Discord", value="aide_discord"),
                discord.SelectOption(label="Obtenir le rôle ✅ | Compte vérifié", value="verif_role")
            ],
            custom_id="ticket_menu"
        )

        view = discord.ui.View()
        view.add_item(menu)

        msg = await salon.send("Choisis une option ci-dessous pour créer un ticket :", view=view)
        await interaction.response.send_message(f"Menu de création de ticket envoyé dans {salon.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
