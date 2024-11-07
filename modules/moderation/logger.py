import discord
import logging
from discord import app_commands
from discord.ext import commands
from collections import deque

# logs dans un fichier 
logging.basicConfig(level=logging.INFO, filename='bot_logs.txt', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Logger(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.command_logs = deque(maxlen=100)  # Conserver les 100 dernières commandes

    # capturer les interactions + slash commands
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.application_command:
            user = interaction.user
            command = interaction.data['name']
            guild = interaction.guild.name if interaction.guild else "DM"
            
            log_message = f"Commande: {command}, Utilisateur: {user}, Serveur: {guild}"
            self.command_logs.append(log_message)  # ajouter le log à la deque
            logging.info(log_message)
            print(log_message)

    @app_commands.command(name="logs", description="Affiche les dernières commandes utilisées")
    @app_commands.describe(num="Le nombre de dernières commandes à afficher")
    async def logs(self, interaction: discord.Interaction, num: int):
        """ 
            Affiche les dernières commandes utilisées 
        """
        if not interaction.user.id == 310120505631834113:
            await interaction.response.send_message("Tu dois être Tsuna pour voir les logs !", ephemeral=True)
            return

        if not interaction.user.guild_permissions.view_audit_log:
            await interaction.response.send_message("Vous n'avez pas la permission de bannir des membres.", ephemeral=True)
            return

        if num < 1:
            await interaction.response.send_message("Veuillez entrer un nombre positif.", ephemeral=True)
            return

        logs_to_display = list(self.command_logs)[-num:]  # dernieres logs

        if not logs_to_display:
            await interaction.response.send_message("Aucun log disponible.", ephemeral=True)
            return

        logs_message = "\n".join(logs_to_display)
        await interaction.response.send_message(f"Dernières commandes utilisées:\n```\n{logs_message}\n```", ephemeral=False)

async def setup(bot):
    await bot.add_cog(Logger(bot))
