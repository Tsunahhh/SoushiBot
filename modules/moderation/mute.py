import discord
from discord import app_commands
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.muted_role = None  # défini plus tard

    async def setup_muted_role(self, guild: discord.Guild):
        """ 
            Crée ou récupère le rôle 'Muted' et lui enlève les permissions d'écriture. 
        """
        muted_role = discord.utils.get(guild.roles, name="Muted")
        
        if muted_role is None:
            muted_role = await guild.create_role(name="Muted", reason="Créer un rôle pour mute les utilisateurs")
            for channel in guild.channels:
                await channel.set_permissions(muted_role, 
                    send_messages=False, 
                    speak=False,
                    add_reactions=False)
        self.muted_role = muted_role

    @app_commands.command(name="mute", description="Mute un utilisateur du serveur")
    @app_commands.describe(user="L'utilisateur à mute", reason="La raison du mute")
    async def mute(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison fournie"):
        """
        Ajoute le rôle 'Muted' à l'utilisateur.
        """
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("Vous n'avez pas la permission de mute des membres.", ephemeral=True)
            return

        if self.muted_role is None:
            await self.setup_muted_role(interaction.guild)

        if self.muted_role in user.roles:
            await interaction.response.send_message(f"{user.mention} est déjà mute.", ephemeral=True)
            return

        try:
            await user.add_roles(self.muted_role, reason=reason)
            await interaction.response.send_message(f"{user.mention} a été mute pour la raison : {reason}.", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message(f"Je ne peux pas mute {user.mention}, car il/elle a un rôle supérieur au mien.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur est survenue : {str(e)}", ephemeral=True)

    @app_commands.command(name="unmute", description="Unmute un utilisateur du serveur")
    @app_commands.describe(user="L'utilisateur à unmute")
    async def unmute(self, interaction: discord.Interaction, user: discord.Member):
        """
            Retire le rôle 'Muted' à l'utilisateur.
        """
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("Vous n'avez pas la permission de mute des membres.", ephemeral=True)
            return

        if self.muted_role is None or self.muted_role not in user.roles:
            await interaction.response.send_message(f"{user.mention} n'est pas mute.", ephemeral=True)
            return

        try:
            await user.remove_roles(self.muted_role, reason="Unmute par commande")
            await interaction.response.send_message(f"{user.mention} a été unmute.", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message(f"Je ne peux pas unmute {user.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur est survenue : {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mute(bot))
