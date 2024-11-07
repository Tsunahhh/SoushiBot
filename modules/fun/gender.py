import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

class GenderLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gender", description="Détermine le genre probable en fonction d'un prénom.")
    @app_commands.describe(name="Prénom de la personne à analyser")
    async def gender(self, interaction: discord.Interaction, name: str):
        """
        Commande pour obtenir le genre probable d'une personne à partir de son prénom.
        """
        url = f"https://api.genderize.io/?name={name}"  # URL de l'API
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                
                    name = data.get("name", "Non disponible")
                    gender = data.get("gender", "Non déterminé")
                    probability = data.get("probability", 0.0)
                    count = data.get("count", 0)

                    probability_percentage = round(probability * 100, 2)
                    
                    try:
                        embed = discord.Embed(
                            title=f"Genre probable pour le prénom : {name.capitalize()}",
                            color=discord.Color.purple()
                        )
                        embed.add_field(name="Genre", value=gender.capitalize(), inline=True)
                        embed.add_field(name="Probabilité", value=f"{probability_percentage}%", inline=True)
                        embed.add_field(name="Nombre d'occurrences", value=count, inline=True)
                        
                        await interaction.response.send_message(embed=embed)
                    except:
                        await interaction.response.send_message("Aucune information sur le nom/pseudo")
                    
                        
                else:
                    await interaction.response.send_message(
                        "Impossible de récupérer les informations pour ce prénom."
                    )

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(GenderLookup(bot))
