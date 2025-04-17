import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput
import asyncio
from datetime import timedelta

# ID du rôle OB
OB_ROLE_ID = 1339286435475230800

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commandes de modération

    @app_commands.command(name='kick', description='Expulse un joueur du serveur')
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def kick(self, interaction: discord.Interaction, joueur: discord.Member):
        modal = ReasonModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        reason = modal.reason.value
        await joueur.kick(reason=reason)

        embed = discord.Embed(
            title="Vous avez été expulsé de notre serveur d'OB",
            description=f"Expulsé par : {interaction.user.name}\nRaison : {reason}",
            colour=0xab0303
        )
        await self.send_sanction_message(interaction, joueur, embed, "expulsé")
        await interaction.followup.send(f'{joueur.mention} a été expulsé.')

    @app_commands.command(name='ban', description='Bannit un joueur du serveur')
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ban(self, interaction: discord.Interaction, joueur: discord.Member, durée: int):
        modal = ReasonModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        reason = modal.reason.value
        await joueur.ban(reason=reason)

        embed = discord.Embed(
            title="Vous avez été banni de notre serveur d'OB",
            description=f"Banni par : {interaction.user.name}\nRaison : {reason}\nDurée : {durée} minutes",
            colour=0xab0303
        )
        await self.send_sanction_message(interaction, joueur, embed, "banni")
        await interaction.followup.send(f'{joueur.mention} a été banni.')

        await asyncio.sleep(durée * 60)
        await interaction.guild.unban(joueur)

    @app_commands.command(name='unban', description='Débannit un joueur du serveur')
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def unban(self, interaction: discord.Interaction, joueur: str):
        banned_users = await interaction.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == tuple(joueur.split('#')):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'{user.mention} a été débanni.')
                return
        await interaction.response.send_message(f'Utilisateur {joueur} non trouvé dans la liste des bannis.')

    @app_commands.command(name='mute', description='Rend muet un joueur du serveur')
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def mute(self, interaction: discord.Interaction, joueur: discord.Member, durée: int):
        modal = ReasonModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        reason = modal.reason.value
        await joueur.timeout(timedelta(minutes=durée), reason=reason)

        embed = discord.Embed(
            title="Vous avez été rendu muet sur notre serveur d'OB",
            description=f"Rendu muet par : {interaction.user.name}\nRaison : {reason}\nDurée : {durée} minutes",
            colour=0xab0303
        )
        await self.send_sanction_message(interaction, joueur, embed, "rendu muet")
        await interaction.followup.send(f'{joueur.mention} a été rendu muet.')

    # Commandes de tickets

    @app_commands.command(name='ticket set', description="Crée un ticket")
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ticket_set(self, interaction: discord.Interaction):
        # Code pour créer un ticket
        pass

    @app_commands.command(name='ticket fermer', description="Ferme un ticket")
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ticket_fermer(self, interaction: discord.Interaction):
        # Code pour fermer un ticket
        pass

    @app_commands.command(name='ticket ouvrir', description="Ouvre un ticket")
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ticket_ouvrir(self, interaction: discord.Interaction):
        # Code pour ouvrir un ticket
        pass

    async def send_sanction_message(self, interaction: discord.Interaction, joueur: discord.Member, embed: discord.Embed, sanction_type: str):
        try:
            await joueur.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(
                f"Impossible d'envoyer un message privé à {joueur.mention}."
            )

class ReasonModal(Modal, title="Raison de la sanction"):
    reason = TextInput(label="Raison", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Merci, la raison a été enregistrée.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Commands(bot))
