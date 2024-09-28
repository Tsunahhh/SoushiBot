import discord
from discord import app_commands
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="avatar", description="Affiche la photo de profil d'un utilisateur")
    @app_commands.describe(user="L'utilisateur dont vous souhaitez voir la photo de profil")
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None):
        """
            Affiche la photo de profil de l'utilisateur spécifié, ou de l'utilisateur qui a lancé la commande.
        """
        if user is None:
            user = interaction.user
        avatar_url = user.display_avatar.url
        embed = discord.Embed(title=f"Photo de profil de {user.name}")
        embed.set_image(url=avatar_url) 
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Avatar(bot))
