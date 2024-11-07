import discord
from discord import app_commands
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="say", description="Parler avec le bot")
    async def say(self, interaction: discord.Interaction, msg: str) -> None:
        """
            Say somethings with the bot
        """
        await interaction.channel.send(msg)
        await interaction.response.send_message(msg + " a été envoyé! ", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Say(bot))