import discord
from discord.ext import commands

OB_ROLE_ID = 1339286435475230800
TICKET_CATEGORY_ID = 1339333886043230218
TICKET_NOTIFICATION_CHANNEL_ID = 1339334513658167397

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_message_id = None  # Message de menu

    @commands.command(name="ticket set", help="Réservé aux admins !")
    async def ticket_set(self, ctx):
        if not any(role.id == OB_ROLE_ID for role in ctx.author.roles):
            return await ctx.send("Tu sais pas lire ? Y'a écrit que c'est pour les admins !")

        await self.send_ticket_menu(ctx)
        await ctx.send("✅ Menu de ticket envoyé.")

    @commands.command(name="ticket ouvrir", help="Admin | Ouvrir un ticket pour un membre")
    @commands.describe(membre="Membre pour ouvrir un ticket")
    async def ticket_ouvrir(self, ctx, membre: discord.Member):
        if not any(role.id == OB_ROLE_ID for role in ctx.author.roles):
            return await ctx.send("Tu sais pas lire ? Y'a écrit que c'est pour les admins !")

        await self.create_ticket(ctx.guild, membre, "Ticket ouvert par un membre de l'OB")
        await ctx.send(f"✅ Ticket ouvert pour {membre.mention}.")

    @commands.command(name="ticket fermer", help="Admin | Fermer un ticket")
    async def ticket_fermer(self, ctx):
        if ctx.channel.category_id == TICKET_CATEGORY_ID:
            await ctx.channel.delete()
            await ctx.send("✅ Le ticket a été fermé.")
        else:
            await ctx.send("❌ T'es pas dans un ticket fréro")

    @commands.command(name="ticket ajouter", help="Admin | Ajouter un membre au ticket")
    @commands.describe(membre="Membre à ajouter")
    async def ticket_ajouter(self, ctx, membre: discord.Member):
        if not any(role.id == OB_ROLE_ID for role in ctx.author.roles):
            return await ctx.send("Tu sais pas lire ? Y'a écrit que c'est pour les admins !")

        if ctx.channel.category_id == TICKET_CATEGORY_ID:
            await ctx.channel.set_permissions(membre, view_channel=True, send_messages=True)
            await ctx.send(f"✅ {membre.mention} ajouté au ticket.")
        else:
            await ctx.send("❌ T'es pas dans un ticket fréro")

    async def send_ticket_menu(self, ctx):
        embed = discord.Embed(title="📩 Ouvrir un Ticket", description="Choisis le type de ticket à créer.", color=0x00ffcc)
        view = TicketMenuView()
        msg = await ctx.send(embed=embed, view=view)
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

async def setup(bot):
    await bot.add_cog(Ticket(bot))
