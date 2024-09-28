import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="pong ! ms")
    async def ping(self, interaction: discord.Interaction):
        """
        Simple command to test the reactivity of the discord bot
        """
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {latency} ms", ephemeral=True)

# Fonction de setup attendue pour les cogs
async def setup(bot):
    await bot.add_cog(Ping(bot))
