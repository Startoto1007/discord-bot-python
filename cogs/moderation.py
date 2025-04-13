import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', help='Expulse un membre du serveur')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Expulse un membre du serveur"""
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} a été expulsé.')

    @commands.command(name='ban', help='Bannit un membre du serveur')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bannit un membre du serveur"""
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} a été banni.')

    @commands.command(name='unban', help='Débannit un membre du serveur')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Débannit un membre du serveur"""
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == tuple(member.split('#')):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} a été débanni.')
                return

async def setup(bot):
    await bot.add_cog(Moderation(bot))
