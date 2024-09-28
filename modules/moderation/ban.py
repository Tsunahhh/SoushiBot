import discord
from discord import app_commands
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="ban", description="Bannir un utilisateur définitivement du serveur !")
    @app_commands.describe(user="L'utilisateur à bannir", reason="Raison pour laquelle l'utilisateur est banni !")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Aucune raison donnée"):
        """
            Bannir un utilisateur du serveur.
        """
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Vous n'avez pas la permission pour ban cet utilisateur !")
            return
        try:
            await user.ban(reason=reason)
            await interaction.response.send_message(f"{user.mention} a été banni du server pour {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(f"Je ne peux pas bannir cet utilisateur !")
        except Exception as e:
            await interaction.response.send_message("Une erreur est survenue : ", str(e))

async def setup(bot):
    await bot.add_cog(Ban(bot))