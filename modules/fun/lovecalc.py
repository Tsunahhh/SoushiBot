import discord
from discord import app_commands
from discord.ext import commands
import random

from entity.lovecalc_db import LoveCalcDB  

class LoveCalc(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.db = LoveCalcDB() 

    @app_commands.command(name="lovecalc", description="Calcule le pourcentage d'amour entre deux utilisateurs.")
    @app_commands.describe(user1="Premier utilisateur", user2="Deuxième utilisateur")
    async def lovecalc(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        """
        Calcule et renvoie le pourcentage d'amour entre deux utilisateurs.
        """
        love_percent = self.db.get_love_percent(str(user1.id), str(user2.id))
        
        if love_percent is None:
            love_percent = random.randint(0, 100)
            self.db.save_love_percent(str(user1.id), str(user2.id), love_percent)
        
        await interaction.response.send_message(
            f"💘 **{user1.display_name}** et **{user2.display_name}** sont compatibles à {love_percent}% !"
        )

    def cog_unload(self):
        self.db.close()

async def setup(bot):
    await bot.add_cog(LoveCalc(bot))
