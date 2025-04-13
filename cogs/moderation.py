import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kick', description='Expulse un membre du serveur')
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Expulse un membre du serveur"""
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member.mention} a été expulsé.')

    @app_commands.command(name='ban', description='Bannit un membre du serveur')
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Bannit un membre du serveur"""
        await member.ban(reason=reason)
        await interaction.response.send_message(f'{member.mention} a été banni.')

    @app_commands.command(name='unban', description='Débannit un membre du serveur')
    @app_commands.default_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: str):
        """Débannit un membre du serveur"""
        banned_users = await interaction.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == tuple(member.split('#')):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'{user.mention} a été débanni.')
                return

async def setup(bot):
    await bot.add_cog(Moderation(bot))
