import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import urllib.parse

class TTS(commands.Cog): 
    def __init__(self, bot) -> None:
        self.bot = bot

    async def join_voice_and_speak(self, interaction: discord.Interaction, text: str, langage: str, msg: str) -> None:
        member = interaction.user

        if member.voice is None:
            await interaction.response.send_message("<!> Vous devez être dans un canal vocal pour utiliser cette commande <!>", ephemeral=True)
            return

        channel = member.voice.channel
        voice_client = await channel.connect()

        phrases = text.split('.')

        async def play_next_sentence():
            for sentence in phrases:
                sentence = sentence.strip()
                if sentence:
                    url = f"http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(sentence)}&tl={langage}"
                    voice_client.play(discord.FFmpegPCMAudio(url))

                    while voice_client.is_playing():
                        await asyncio.sleep(1)

        await interaction.response.send_message(msg, ephemeral=True)
        await play_next_sentence()
        await voice_client.disconnect()


    @app_commands.command(name="ttsfr", description="Parler avec le bot dans la voc !")
    async def tts_fr(self, interaction: discord.Interaction, text: str):
        await self.join_voice_and_speak(interaction, text, 'fr', "J'arrive tout de suite !")

    @app_commands.command(name="ttsen", description="Speak in the voice channel with the bot !")
    async def tts_en(self, interaction: discord.Interaction, text: str):
        await self.join_voice_and_speak(interaction, text, 'en', "I m comming bro !")

async def setup(bot):
    await bot.add_cog(TTS(bot))