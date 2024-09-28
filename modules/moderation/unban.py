import discord
from discord import app_commands
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Commande de débannissement
    @app_commands.command(name="unban", description="Débannir un utilisateur du serveur")
    @app_commands.describe(user_id="L'ID de l'utilisateur à débannir", reason="Raison du débannissement")
    async def unban(self, interaction: discord.Interaction, user_id: int, reason: str = "Aucune raison fournie"):
        """
            Débannir un utilisateur du serveur via son ID.
        """
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Vous n'avez pas la permission de débannir des membres.", ephemeral=True)
            return

        try:
            user = await interaction.guild.fetch_ban(discord.Object(id=user_id))
        except discord.NotFound:
            await interaction.response.send_message(f"Aucun utilisateur avec l'ID {user_id} n'est banni.", ephemeral=True)
            return
        
        try:
            await interaction.guild.unban(user.user, reason=reason)
            await interaction.response.send_message(f"{user.user.mention} a été débanni.", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message(f"Je n'ai pas la permission de débannir {user.user.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur est survenue : {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Unban(bot))
