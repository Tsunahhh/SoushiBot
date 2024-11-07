import discord
from discord import app_commands
from discord.ext import commands
import aiohttp  # Pour les requêtes HTTP asynchrones

class Joke(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="joke", description="Donne une blague aléatoire d'internet")
    async def joke(self, interaction: discord.Interaction):
        """
        Récupère une blague aléatoire à partir d'une API et l'envoie en réponse.
        """
        url = "https://official-joke-api.appspot.com/random_joke"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    joke_setup = data['setup']
                    joke_punchline = data['punchline']

                    # Envoi de la blague sous forme de message
                    await interaction.response.send_message(f"😂 **Blague** : {joke_setup} \n\n**Punchline** : {joke_punchline}")
                else:
                    # En cas d'erreur avec l'API
                    await interaction.response.send_message("Désolé, je n'ai pas pu trouver de blague cette fois-ci.")

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(Joke(bot))
