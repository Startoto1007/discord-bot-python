import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput
import asyncio
from datetime import timedelta

# ID du rôle OB
OB_ROLE_ID = 1339286435475230800
TICKET_CATEGORY_ID = 1339333886043230218  # Remplace avec l'ID de la catégorie de tickets

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

    @app_commands.command(name='ticket_set', description="Crée un ticket")
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ticket_set(self, interaction: discord.Interaction):
        """Créer un salon de ticket"""
        if not self._is_ob_member(interaction.user):
            await interaction.response.send_message("Vous devez être un membre de l'OB pour utiliser cette commande.")
            return

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }

        # Créer un salon dans la catégorie des tickets
        category = discord.utils.get(interaction.guild.categories, id=TICKET_CATEGORY_ID)
        ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', category=category, overwrites=overwrites)

        await ticket_channel.send(f'Bonjour {interaction.user.mention}, votre ticket a été créé. Un membre de l\'équipe OB va vous assister dès que possible.')
        await interaction.response.send_message(f'Votre ticket a été créé dans {ticket_channel.mention}.')

    @app_commands.command(name='ticket_fermer', description="Ferme un ticket")
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ticket_fermer(self, interaction: discord.Interaction):
        """Fermer un ticket"""
        if not self._is_ob_member(interaction.user):
            await interaction.response.send_message("Vous devez être un membre de l'OB pour utiliser cette commande.")
            return

        # Vérifie si le salon est un ticket
        if interaction.channel.category and interaction.channel.category.id == TICKET_CATEGORY_ID:
            await interaction.channel.delete()
            await interaction.response.send_message(f"Le ticket {interaction.channel.mention} a été fermé.")
        else:
            await interaction.response.send_message("Cette commande ne peut être utilisée que dans un salon de ticket.")

    @app_commands.command(name='ticket_ouvrir', description="Ouvre un ticket")
    @app_commands.checks.has_role(OB_ROLE_ID)
    async def ticket_ouvrir(self, interaction: discord.Interaction):
        """Ouvrir un ticket existant"""
        if not self._is_ob_member(interaction.user):
            await interaction.response.send_message("Vous devez être un membre de l'OB pour utiliser cette commande.")
            return

        # Vérifie si le salon est un ticket fermé et peut être rouvert
        if interaction.channel.category and interaction.channel.category.id == TICKET_CATEGORY_ID:
            await interaction.channel.edit(name=f'ticket-{interaction.user.name}')
            await interaction.response.send_message(f"Le ticket {interaction.channel.mention} a été rouvert.")
        else:
            await interaction.response.send_message("Cette commande ne peut être utilisée que dans un salon de ticket fermé.")

    async def send_sanction_message(self, interaction: discord.Interaction, joueur: discord.Member, embed: discord.Embed, sanction_type: str):
        try:
            await joueur.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(
                f"Impossible d'envoyer un message privé à {joueur.mention}."
            )

    def _is_ob_member(self, member):
        """Vérifie si un membre a le rôle OB"""
        return any(role.id == OB_ROLE_ID for role in member.roles)

class ReasonModal(Modal, title="Raison de la sanction"):
    reason = TextInput(label="Raison", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Merci, la raison a été enregistrée.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Commands(bot))
await bot.add_cog(Commands(bot))
