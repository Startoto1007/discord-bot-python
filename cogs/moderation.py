import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput
import asyncio
from datetime import timedelta

# ID du rôle OB
OB_ROLE_ID = 1339286435475230800

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kick', description='Expulse un joueur du serveur')
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def kick(self, interaction: discord.Interaction, joueur: discord.Member):
        """Expulse un joueur du serveur"""
        modal = ReasonModal(title="Raison de l'expulsion")
        await interaction.response.send_modal(modal)
        await modal.wait()

        reason = modal.reason.value
        await joueur.kick(reason=reason)

        # Création de l'embed de notification
        embed = discord.Embed(
            title="Vous avez été expulsé de notre serveur d'OB",
            description=f"Expulsé par : {interaction.user.name}\nRaison : {reason}",
            colour=0xab0303
        )

        # Envoi du message à l'utilisateur sanctionné
        await self.send_sanction_message(interaction, joueur, embed, "expulsé")

        # Confirmation du kick dans le canal de l'interaction
        await interaction.followup.send(f'{joueur.mention} a été expulsé.')

    @app_commands.command(name='ban', description='Bannit un joueur du serveur')
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ban(self, interaction: discord.Interaction, joueur: discord.Member, durée: int):
        """Bannit un joueur du serveur"""
        modal = ReasonModal(title="Raison du bannissement")
        await interaction.response.send_modal(modal)
        await modal.wait()

        reason = modal.reason.value
        await joueur.ban(reason=reason)

        # Création de l'embed de notification
        embed = discord.Embed(
            title="Vous avez été banni de notre serveur d'OB",
            description=f"Banni par : {interaction.user.name}\nRaison : {reason}\nDurée : {durée} minutes",
            colour=0xab0303
        )
        
        # Envoi du message à l'utilisateur sanctionné
        await self.send_sanction_message(interaction, joueur, embed, "banni")

        # Confirmation du ban dans le canal de l'interaction
        await interaction.followup.send(f'{joueur.mention} a été banni.')

        # Débannir après la durée spécifiée
        await asyncio.sleep(durée * 60)
        await interaction.guild.unban(joueur)

    @app_commands.command(name='unban', description='Débannit un joueur du serveur')
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def unban(self, interaction: discord.Interaction, joueur: str):
        """Débannit un joueur du serveur"""
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
        """Rend muet un joueur du serveur"""
        modal = ReasonModal(title="Raison du mute")
        await interaction.response.send_modal(modal)
        await modal.wait()

        reason = modal.reason.value
        await joueur.timeout(timedelta(minutes=durée), reason=reason)

        # Création de l'embed de notification
        embed = discord.Embed(
            title="Vous avez été rendu muet sur notre serveur d'OB",
            description=f"Rendu muet par : {interaction.user.name}\nRaison : {reason}\nDurée : {durée} minutes",
            colour=0xab0303
        )

        # Envoi du message à l'utilisateur sanctionné
        await self.send_sanction_message(interaction, joueur, embed, "rendu muet")

        # Confirmation du mute dans le canal de l'interaction
        await interaction.followup.send(f'{joueur.mention} a été rendu muet.')

    async def send_sanction_message(self, interaction: discord.Interaction, joueur: discord.Member, embed: discord.Embed, sanction_type: str):
        """Envoie un message de sanction à l'utilisateur"""
        try:
            await joueur.send(embed=embed)
        except discord.Forbidden:
            # Si le bot ne peut pas envoyer de message privé, envoyer un message dans le canal de l'interaction
            await interaction.followup.send(f"Impossible d'envoyer un message privé à {joueur.mention}. Assurez-vous que le bot a les permissions nécessaires et que l'utilisateur accepte les messages privés.")

class ReasonModal(Modal):
    def __init__(self, title: str):
        super().__init__(title=title)
        self.reason = TextInput(label="Raison", required=True)
        self.add_item(self.reason)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
