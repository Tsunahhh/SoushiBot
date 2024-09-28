import discord
from discord import app_commands
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="clear", description="Supprime les derniers messages du canal")
    @app_commands.describe(amount="Le nombre de messages à supprimer")
    async def clear(self, interaction: discord.Interaction, amount: int):
        """
            Supprime les derniers messages du canal.
        """

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Vous n'avez pas la permission de gérer les messages.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.manage_messages:
            await interaction.response.send_message("Je n'ai pas la permission de gérer les messages.", ephemeral=True)
            return

        if amount <= 0:
            await interaction.response.send_message("Veuillez spécifier un nombre de messages supérieur à 0.", ephemeral=True)
            return
        if amount > 100:  
            await interaction.response.send_message("Vous ne pouvez pas supprimer plus de 100 messages à la fois.", ephemeral=True)
            return
    
        await interaction.response.send_message("Je vais supprimer {} messages !".format(amount), ephemeral=True)

        deleted = await interaction.channel.purge(limit=amount + 1)
        await interaction.channel.send(f"J'ai supprimé {len(deleted - 1)} messages.")  

async def setup(bot):
    await bot.add_cog(Clear(bot))
