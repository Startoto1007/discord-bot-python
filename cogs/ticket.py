import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_id = 1339333886043230218
        self.notification_channel_id = 1339334513658167397
        self.role_ob_id = 1339286435475230800

    @app_commands.command(name="ticket_set", description="Configurer le système de tickets")
    async def ticket_set(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 Créer un ticket",
            description="Clique sur le bouton ci-dessous pour créer un ticket.",
            color=discord.Color.blurple()
        )
        view = TicketButtonView()
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="ticket_fermer", description="Ferme le ticket actuel")
    async def ticket_fermer(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Cette commande ne peut être utilisée que dans un ticket.", ephemeral=True)

        await interaction.channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await interaction.response.send_message("✅ Ticket fermé.", ephemeral=True)

    @app_commands.command(name="ticket_ouvrir", description="Rouvre un ticket fermé")
    async def ticket_ouvrir(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Cette commande ne peut être utilisée que dans un ticket.", ephemeral=True)

        await interaction.channel.set_permissions(interaction.guild.default_role, view_channel=True)
        await interaction.response.send_message("✅ Ticket rouvert.", ephemeral=True)

    @app_commands.command(name="ticket_ajouter", description="Ajouter un membre au ticket")
    @app_commands.describe(membre="Membre à ajouter dans le salon de ticket")
    async def ticket_ajouter(self, interaction: discord.Interaction, membre: discord.Member):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Cette commande ne peut être utilisée que dans un ticket.", ephemeral=True)

        await interaction.channel.set_permissions(membre, view_channel=True, send_messages=True)
        await interaction.response.send_message(f"✅ {membre.mention} a été ajouté au ticket.", ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component and interaction.data["custom_id"] == "create_ticket":
            await interaction.response.send_modal(TicketReasonModal(self))


class TicketButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Créer un ticket", custom_id="create_ticket", style=discord.ButtonStyle.green))


class TicketReasonModal(Modal, title="Créer un ticket"):
    raison = TextInput(label="Pourquoi veux-tu créer un ticket ?", style=discord.TextStyle.paragraph, required=True)

    def __init__(self, cog: Ticket):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        auteur = interaction.user
        role_ob = discord.Object(id=self.cog.role_ob_id)

        # Vérification du rôle OB
        if role_ob.id not in [role.id for role in auteur.roles]:
            await interaction.response.send_message("❌ Tu dois faire partie de l’OB pour créer un ticket.", ephemeral=True)
            return

        guild = interaction.guild
        category = guild.get_channel(self.cog.category_id)
        support_role = guild.get_role(self.cog.role_ob_id)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            auteur: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            support_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{auteur.name}",
            category=category,
            overwrites=overwrites
        )

        await ticket_channel.send(f"{auteur.mention}, un membre de l'équipe va bientôt te répondre.")
        await interaction.response.send_message(f"✅ Ton ticket a été créé ici : {ticket_channel.mention}", ephemeral=True)

        notif_channel = guild.get_channel(self.cog.notification_channel_id)
        embed = discord.Embed(
            title="🎫 Nouveau ticket",
            description=f"{auteur.mention} a ouvert un ticket.",
            color=discord.Color.green()
        )
        embed.add_field(name="Raison", value=self.raison.value, inline=False)
        await notif_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Ticket(bot))
