import discord
from discord.ext import commands
from discord import app_commands

OB_ROLE_ID = 1339286435475230800
TICKET_CATEGORY_ID = 1339333886043230218
TICKET_NOTIFICATION_CHANNEL_ID = 1339334513658167397

intents = discord.Intents.default()
intents.message_content = True  # Pour permettre d'écouter le contenu des messages

bot = commands.Bot(command_prefix="!", intents=intents)  # Préfixe pour les commandes classiques, mais tu n'en as pas besoin pour les commandes slash

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_message_id = None  # Message de menu

    @app_commands.command(name="ticket set", description="Réservé aux admins !")
    async def ticket_set(self, interaction: discord.Interaction):
        if not any(role.id == OB_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("Tu sais pas lire ? Y'a écrit que c'est pour les admins !", ephemeral=True)

        await self.send_ticket_menu(interaction)
        await interaction.response.send_message("✅ Menu de ticket envoyé.", ephemeral=True)

    @app_commands.command(name="ticket ouvrir", description="Admin | Ouvrir un ticket pour un membre")
    @app_commands.describe(membre="Membre pour ouvrir un ticket")
    async def ticket_ouvrir(self, interaction: discord.Interaction, membre: discord.Member):
        if not any(role.id == OB_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("Tu sais pas lire ? Y'a écrit que c'est pour les admins !", ephemeral=True)

        await self.create_ticket(interaction.guild, membre, "Ticket ouvert par un membre de l'OB")
        await interaction.response.send_message(f"✅ Ticket ouvert pour {membre.mention}.", ephemeral=True)

    @app_commands.command(name="ticket fermer", description="Admin | Fermer un ticket")
    async def ticket_fermer(self, interaction: discord.Interaction):
        if interaction.channel.category_id == TICKET_CATEGORY_ID:
            await interaction.channel.delete()
            await interaction.response.send_message("✅ Le ticket a été fermé.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ T'es pas dans un ticket fréro", ephemeral=True)

    @app_commands.command(name="ticket ajouter", description="Admin | Ajouter un membre au ticket")
    @app_commands.describe(membre="Membre à ajouter")
    async def ticket_ajouter(self, interaction: discord.Interaction, membre: discord.Member):
        if not any(role.id == OB_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("Tu sais pas lire ? Y'a écrit que c'est pour les admins !", ephemeral=True)

        if interaction.channel.category_id == TICKET_CATEGORY_ID:
            await interaction.channel.set_permissions(membre, view_channel=True, send_messages=True)
            await interaction.response.send_message(f"✅ {membre.mention} ajouté au ticket.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ T'es pas dans un ticket fréro", ephemeral=True)

    async def send_ticket_menu(self, interaction):
        embed = discord.Embed(title="📩 Ouvrir un Ticket", description="Choisis le type de ticket à créer.", color=0x00ffcc)
        view = TicketMenuView()
        msg = await interaction.channel.send(embed=embed, view=view)
        self.ticket_message_id = msg.id

    async def create_ticket(self, guild, user, raison):
        category = guild.get_channel(TICKET_CATEGORY_ID)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.get_role(OB_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category,
            overwrites=overwrites,
            topic=f"Ticket de {user} : {raison}"
        )

        embed = discord.Embed(
            title="🎟️ Nouveau Ticket",
            description=f"{user.mention} a ouvert un ticket : **{raison}**",
            color=0x3498db
        )
        embed.set_footer(text="Un membre de l’OB va te répondre sous peu.")

        await channel.send(content=f"{user.mention}", embed=embed)

        # Notifie l'OB
        notif_channel = guild.get_channel(TICKET_NOTIFICATION_CHANNEL_ID)
        if notif_channel:
            await notif_channel.send(f"📬 Ticket ouvert par {user.mention} : {channel.mention}")

class TicketMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketTypeSelect())

class TicketTypeSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Signaler un problème dans le PW de l’OB Zelda", value="probleme_pw"),
            discord.SelectOption(label="Demander de l’aide sur Discord", value="aide_discord"),
            discord.SelectOption(label="Obtenir le rôle Compte vérifié", value="compte_verifie")
        ]
        super().__init__(placeholder="Choisis un type de ticket", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        raison = {
            "probleme_pw": "Problème dans le PW de l’OB Zelda",
            "aide_discord": "Demande d’aide sur Discord",
            "compte_verifie": "Demande du rôle Compte vérifié"
        }.get(self.values[0], "Demande inconnue")

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.client.get_cog("Ticket").create_ticket(interaction.guild, interaction.user, raison)
        await interaction.followup.send("🎫 Ton ticket a été créé !", ephemeral=True)

# Code pour charger le cog
async def setup(bot):
    await bot.add_cog(Ticket(bot))

# Lancer le bot
bot.run("VOTRE_TOKEN")
