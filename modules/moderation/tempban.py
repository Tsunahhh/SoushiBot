import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class TempBan(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="tempban", description="Bannit temporairement un utilisateur")
    @app_commands.describe(user="L'utilisateur à bannir", duration="Durée du ban (en secondes)", reason="La raison du ban")
    async def tempban(self, interaction: discord.Interaction, user: discord.Member, duration: int, reason: str = "Aucune raison fournie"):
        """
            Bannit un utilisateur pour une durée spécifiée.
        """
        # user a permission de bannir des membres
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Vous n'avez pas la permission de bannir des membres.", ephemeral=True)
            return

        # bot a la permission de bannir des membres
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message("Je n'ai pas la permission de bannir des membres.", ephemeral=True)
            return

        # victime a un rôle > au bot
        if user.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(f"Je ne peux pas bannir {user.mention}, car il/elle a un rôle supérieur au mien.", ephemeral=True)
            return

        # bannir
        try:
            await user.ban(reason=reason)
            await interaction.response.send_message(f"{user.mention} a été banni pour {duration} secondes. Raison : {reason}.", ephemeral=False)
            
            # attendre la durée spécifiée
            await asyncio.sleep(duration)
            
            # déban l'utilisateur après la durée
            await interaction.guild.unban(user)
            
            print(f"{user} a été débanni après {duration} secondes.")
        except discord.Forbidden:
            await interaction.response.send_message(f"Je ne peux pas bannir {user.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur est survenue : {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TempBan(bot))
