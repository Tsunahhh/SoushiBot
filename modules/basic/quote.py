import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import ssl

class Quotes(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="quote", description="Donne une citation aléatoire.")
    async def quote(self, interaction: discord.Interaction):
        """
        Renvoie une citation aléatoire à partir d'une API.
        """
        ssl_context = ssl._create_unverified_context()  # Création d'un contexte SSL non vérifié
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.quotable.io/random", ssl=ssl_context) as response:
                if response.status == 200:
                    data = await response.json()
                    quote = data['content']
                    author = data['author']
                    await interaction.response.send_message(f"💬 **Citation** : {quote} - *{author}*")
                else:
                    await interaction.response.send_message("Impossible de récupérer une citation pour le moment.")

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(Quotes(bot))
