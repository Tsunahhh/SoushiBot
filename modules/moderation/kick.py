import discord
from discord import app_commands
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="kick", description="Kick un utilisateur du serveur")
    @app_commands.describe(user="L'utilisateur à kicker", reason="La raison du kick")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison fournie"):
        """
            Kick l'utilisateur du serveur.
        """
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("Vous n'avez pas la permission de kicker des membres.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message("Je n'ai pas la permission de kicker des membres.", ephemeral=True)
            return
        
        if user.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(f"Je ne peux pas kicker {user.mention}, car il/elle a un rôle supérieur au mien.", ephemeral=True)
            return

        try:
            await user.kick(reason=reason)
            await interaction.response.send_message(f"{user.mention} a été kické pour la raison : {reason}.", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message(f"Je ne peux pas kicker {user.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur est survenue : {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Kick(bot))
