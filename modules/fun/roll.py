import discord
from discord import app_commands
from discord.ext import commands
import random

class Dice(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="roll", description="Lance un dé avec un nombre de faces spécifié.")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        """
        Lance un dé avec un nombre de faces spécifié (par défaut, 6).
        """
        if sides < 1:
            await interaction.response.send_message("Le nombre de faces doit être supérieur à 0.")
            return

        result = random.randint(1, sides)  # Lancer le dé
        await interaction.response.send_message(f"🎲 Vous avez lancé un dé à {sides} faces : **{result}**")

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(Dice(bot))

