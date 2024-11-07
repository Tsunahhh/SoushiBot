import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import ssl

class AboutCats(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="aboutcats", description="Donne un fait sur les chats aléatoire.")
    async def about_cats(self, interaction: discord.Interaction):
        """
            Renvoie un fait sur les chats aléatoire à partir d'un API.
        """
        ssl_context = ssl._create_unverified_context()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://catfact.ninja/fact", ssl=ssl_context) as response:
                if response.status == 200:
                    data = await response.json()
                    quote = data['fact']
                    await interaction.response.send_message(f"🐈 **About Cats** : `{quote}`")
                else:
                    await interaction.response.send_message("Impossible de récupérer une citation pour le moment.")

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(AboutCats(bot))