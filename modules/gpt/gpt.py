import discord
from discord.ext import commands
from discord import app_commands
from groq import Groq
from config import *
from entity import gpt_db

class GPT(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.meta = Groq(api_key=GROQ_KEY)
        self.gpt_db = gpt_db.GPTDB()

    @app_commands.command(name="addgpt", description="Ajoute le droit d'utiliser l'IA sur un channel et serveur donné")
    async def addgpt(self, interaction: discord.Interaction):
        if interaction.user.id == 310120505631834113:
            self.gpt_db.insertServerChannel(interaction.guild.id, interaction.channel_id)
            await interaction.response.send_message("Ce channel fait maintenant parti des channels lus par le bot ! ✅", ephemeral=True)

    @app_commands.command(name="delgpt", description="Supprimer le droit d'utiliser l'IA sur un channel et serveur donné")
    async def delgpt(self, interaction: discord.Interaction):
        if interaction.user.id == 310120505631834113:
            self.gpt_db.deleteServerChannel(interaction.guild.id, interaction.channel_id)
            await interaction.response.send_message("C'est bon, je prends ma retraite ! ✅", ephemeral=True)
            await interaction.followup.send("https://tenor.com/view/arabian-cat-arab-cat-desert-desert-cat-gif-2052435309915639736")

    @app_commands.command(name="gpt", description="Donne une réponse générée par l'IA")
    async def gpt(self, interaction: discord.Interaction, msg: str):
        await interaction.response.defer()
        if self.gpt_db.isChanServExist(interaction.guild.id, interaction.channel_id):
            response = self.meta.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": msg  # ou autre contenu approprié
                    }
                ],
                temperature=1,
                max_tokens=2000,
                top_p=1,
                stream=False,
                stop=None,
            )
            res_txt = response.choices[0].message.content

            # Envoie des messages en fragments de 2000 caractères pour respecter les limites de Discord
            while len(res_txt) >= 2000:
                subres = res_txt[:2000]
                res_txt = res_txt[2000:]
                await interaction.followup.send(subres)

            await interaction.followup.send(res_txt)  # Envoie le dernier fragment
        else:
            await interaction.followup.send("Ce channel n'est pas lu par gpt -> contact tawonto pour plus d'informations.")

async def setup(bot):
    await bot.add_cog(GPT(bot))