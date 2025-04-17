import discord
from discord import app_commands
from discord.ext import commands

CATEGORY_ID = 1339333886043230218
NOTIF_CHANNEL_ID = 1339334513658167397
ROLE_OB_ID = 1339286435475230800

class TicketModal(discord.ui.Modal, title="Créer un ticket"):
    raison = discord.ui.TextInput(label="Pourquoi souhaites-tu ouvrir un ticket ?", style=discord.TextStyle.paragraph)

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎟️ Nouvelle demande de ticket",
            description=f"**Auteur :** {interaction.user.mention}\n**Raison :** {self.raison.value}",
            color=discord.Color.blurple()
        )
        view = TicketDecisionView(interaction.user, self.raison.value, interaction.client)
        notif_channel = interaction.client.get_channel(NOTIF_CHANNEL_ID)
        await notif_channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Ta demande a été envoyée à l'équipe !", ephemeral=True)

class TicketDecisionView(discord.ui.View):
    def __init__(self, user: discord.User, reason: str, bot: commands.Bot):
        super().__init__(timeout=None)
        self.user = user
        self.reason = reason
        self.bot = bot

    @discord.ui.button(label="✅ Accepter", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = guild.get_channel(CATEGORY_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            self.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            interaction.user: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
        }

        channel = await guild.create_text_channel(name=f"ticket-{self.user.name}", category=category, overwrites=overwrites)
        await channel.send(f"{self.user.mention}, ton ticket a été accepté. Un membre de l'équipe te répondra ici.")
        await interaction.response.send_message(f"✅ Salon créé : {channel.mention}", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Refuser", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.user.send("❌ Ta demande de ticket a été refusée.")
        except discord.Forbidden:
            await interaction.response.send_message("Impossible d’envoyer un message privé à l’utilisateur.", ephemeral=True)
        else:
            await interaction.response.send_message("Le ticket a été refusé.", ephemeral=True)
        self.stop()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎟️ Ouvrir un ticket", style=discord.ButtonStyle.blurple)
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = TicketModal(interaction)
        await interaction.response.send_modal(modal)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket_set", description="Configurer le bouton pour ouvrir un ticket")
    async def ticket_set(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator and ROLE_OB_ID not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("⛔ Tu n’as pas la permission d’utiliser cette commande.", ephemeral=True)

        embed = discord.Embed(
            title="Besoin d'aide ?",
            description="Clique sur le bouton ci-dessous pour ouvrir un ticket.\nUn membre de l'équipe te répondra rapidement.",
            color=discord.Color.green()
        )
        await interaction.channel.send(embed=embed, view=TicketView())
        await interaction.response.send_message("✅ Bouton envoyé avec succès !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
