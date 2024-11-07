import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

class Bitcoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bitcoin", description="Obtenez le prix actuel du Bitcoin en USD, GBP et EUR.")
    async def bitcoin(self, interaction: discord.Interaction):
        """
        Commande pour obtenir le prix actuel du Bitcoin en différentes devises.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"  # URL de l'API
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extraction des informations nécessaires
                    time_updated = data["time"].get("updated", "Non disponible")
                    disclaimer = data.get("disclaimer", "Non disponible")
                    
                    # Informations sur les taux pour USD, GBP, et EUR
                    bpi_usd = data["bpi"]["USD"]
                    bpi_gbp = data["bpi"]["GBP"]
                    bpi_eur = data["bpi"]["EUR"]

                    # Création d'un message embed pour l'affichage
                    embed = discord.Embed(
                        title="Prix actuel du Bitcoin",
                        description="Prix en temps réel du Bitcoin.",
                        color=discord.Color.gold()
                    )
                    embed.add_field(
                        name="Dernière mise à jour", value=time_updated, inline=False
                    )
                    
                    # Taux en USD
                    embed.add_field(
                        name=f"{bpi_usd['code']} - {bpi_usd['description']}",
                        value=f"$ {bpi_usd['rate']}",
                        inline=True
                    )

                    # Taux en GBP
                    embed.add_field(
                        name=f"{bpi_gbp['code']} - {bpi_gbp['description']}",
                        value=f"£ {bpi_gbp['rate']}",
                        inline=True
                    )

                    # Taux en EUR
                    embed.add_field(
                        name=f"{bpi_eur['code']} - {bpi_eur['description']}",
                        value=f"€ {bpi_eur['rate']}",
                        inline=True
                    )

                    # Ajouter l'avertissement
                    embed.set_footer(text=disclaimer)
                    
                    # Envoi de l'embed comme réponse
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(
                        "Impossible de récupérer les informations sur le Bitcoin pour le moment."
                    )

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(Bitcoin(bot))
