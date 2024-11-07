import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

class IPLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="iplookup", description="Obtenez des informations géographiques sur une adresse IP.")
    @app_commands.describe(ip="Adresse IP à rechercher")
    async def iplookup(self, interaction: discord.Interaction, ip: str):
        """
            Commande pour obtenir des informations sur une adresse IP à partir de l'API ipinfo.io
        """
        url = f"https://ipinfo.io/{ip}/geo"  # URL de l'API
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    ip_address = data.get("ip", "Non disponible")
                    city = data.get("city", "Non disponible")
                    region = data.get("region", "Non disponible")
                    country = data.get("country", "Non disponible")
                    location = data.get("loc", "Non disponible")
                    org = data.get("org", "Non disponible")
                    timezone = data.get("timezone", "Non disponible")

                    embed = discord.Embed(
                        title=f"Informations sur l'IP : {ip_address}",
                        color=discord.Color.blue()
                    )

                    embed.add_field(name="Ville", value=city, inline=True)
                    embed.add_field(name="Région", value=region, inline=True)
                    embed.add_field(name="Pays", value=country, inline=True)
                    embed.add_field(name="Localisation", value=location, inline=True)
                    embed.add_field(name="Organisation", value=org, inline=True)
                    embed.add_field(name="Fuseau horaire", value=timezone, inline=True)
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(
                        "Impossible de récupérer les informations pour cette adresse IP."
                    )

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(IPLookup(bot))
