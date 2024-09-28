import discord
from discord import app_commands
from discord.ext import commands
import random
import os

class Fact(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.facts = self.load_facts()

    def load_facts(self):
        """
        Charge les faits historiques à partir d'un fichier facts.txt.
        """
        facts_file = "facts.txt"
        if os.path.exists(facts_file):
            with open(facts_file, "r", encoding="utf-8") as file:
                # Lit chaque ligne du fichier et retire les espaces blancs ou les sauts de ligne
                facts = [line.strip() for line in file.readlines() if line.strip()]
                return facts
        else:
            # Si le fichier n'existe pas, on retourne une liste vide ou un message par défaut
            return ["Aucun fait historique n'a été trouvé. Assurez-vous que 'facts.txt' est présent."]

    @app_commands.command(name="fact", description="Donne un fait historique aléatoire.")
    async def fact(self, interaction: discord.Interaction):
        """
        Renvoie un fait historique aléatoire à partir du fichier facts.txt.
        """
        # Sélection d'un fait historique aléatoire si des faits sont disponibles
        if self.facts:
            random_fact = random.choice(self.facts)
            await interaction.response.send_message(f"📜 **Fait historique** : {random_fact}")
        else:
            await interaction.response.send_message("Aucun fait n'est disponible pour le moment.")

# Fonction de setup pour ajouter la cog
async def setup(bot):
    await bot.add_cog(Fact(bot))
