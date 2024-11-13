import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
import asyncio
import math  # Ajoutez cette ligne pour utiliser math.ceil()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        self.music_queue = {}  # file d'attente pour chaque serveur
        self.skip_votes = {}  # pour le système de votes
        self.locks = {}

    async def play_next(self, guild_id):
        """Lance la musique suivante dans la file d'attente ou déconnecte le bot si la file est vide."""
        if guild_id not in self.locks:
            self.locks[guild_id] = asyncio.Lock()

        async with self.locks[guild_id]:
            if self.music_queue[guild_id]:
                next_song = self.music_queue[guild_id].pop(0)
                voice_client = self.voice_clients[guild_id]
                try:
                    # Crée la source audio directement depuis l'URL avec les meilleures options FFmpeg
                    source = await discord.FFmpegOpusAudio.from_probe(
                        next_song['url'],
                        before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  # Options pour la meilleure gestion de flux
                        options='-vn -ac 2 -ar 48000 -f opus'  # Meilleures options pour l'audio dans Discord
                    )
                    voice_client.play(source, after=lambda e: self._after_play(e, guild_id))

                    # Annonce la chanson jouée
                    channel = next_song['interaction'].channel
                    await channel.send(f"🎶 Lecture de : **{next_song['title']}**")
                    self.skip_votes[guild_id] = set()

                except Exception as e:
                    # En cas d'erreur, envoyer un message d'erreur et continuer
                    await next_song['interaction'].channel.send(f"Erreur de lecture : {str(e)}")
                    await self.play_next(guild_id)
            else:
                # file vide -> déconnecte le bot
                voice_client = self.voice_clients[guild_id]
                if not getattr(voice_client, "is_leaving", False):
                    await voice_client.disconnect()
                    setattr(voice_client, "is_leaving", True)
                del self.voice_clients[guild_id]

    async def add_to_queue(self, url, interaction):
        """Ajoute une chanson ou une playlist à la file d'attente avec une qualité audio optimale."""
        guild_id = interaction.guild.id

        ydl_opts = {
            'format': 'bestaudio/best', 
            'quiet': True,
            'socket_timeout': 10,  # délais court pour les connexions
            'extractaudio': True,  # sans la vidéo
            'audioquality': 1,  # Meilleure qualité audio
            'outtmpl': './downloads/%(id)s.%(ext)s',  # dossier temporaire
        }

        def extract_info_sync():
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)

        info = await asyncio.to_thread(extract_info_sync)
        if 'entries' in info:  # URL de playlist
            for entry in info['entries']:
                self.music_queue[guild_id].append({
                    'url': entry['url'],
                    'title': entry.get('title', 'Audio'),
                    'interaction': interaction
                })
        else:  # URL de chanson unique
            self.music_queue[guild_id].append({
                'url': info['url'],
                'title': info.get('title', 'Audio'),
                'interaction': interaction
            })

    @app_commands.command(name="play", description="Joue une musique ou une playlist à partir d'une URL YouTube.")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()
        guild_id = interaction.guild.id

        # Vérifie si le bot est déjà connecté à un canal vocal, sinon le fait rejoindre automatiquement
        if guild_id not in self.voice_clients:
            voice_channel = interaction.user.voice.channel
            if voice_channel:
                voice_client = await voice_channel.connect()
                self.voice_clients[guild_id] = voice_client
                self.music_queue[guild_id] = []
                self.skip_votes[guild_id] = set()
            else:
                await interaction.followup.send("Vous devez être dans un canal vocal pour utiliser cette commande.", ephemeral=True)
                return

        # Ajoute la chanson à la file d'attente
        await self.add_to_queue(url, interaction)
        await interaction.followup.send("Ajouté à la file d'attente 🎶")

        # Si aucune musique n'est en cours de lecture, commence à jouer la première chanson de la file
        voice_client = self.voice_clients[guild_id]
        if not voice_client.is_playing():
            await self.play_next(guild_id)

    @app_commands.command(name="skip", description="Vote pour passer la chanson en cours.")
    async def skip(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        voice_client = self.voice_clients.get(guild_id)
        if not voice_client or not voice_client.is_playing():
            await interaction.response.send_message("Aucune musique n'est en cours de lecture.", ephemeral=True)
            return

        # Ajoute un vote de skip
        self.skip_votes[guild_id].add(interaction.user.id)
        channel = interaction.user.voice.channel
        required_votes = math.ceil(len(channel.members) / 2)

        if len(self.skip_votes[guild_id]) >= required_votes:
            voice_client.stop()
            await interaction.response.send_message("⏭️ Passé avec succès à la chanson suivante !", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Vote ajouté pour passer. **{len(self.skip_votes[guild_id])}/{required_votes}** votes nécessaires.",
                ephemeral=True
            )

    @app_commands.command(name="queue", description="Affiche la file d'attente.")
    async def queue(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        if guild_id not in self.music_queue or not self.music_queue[guild_id]:
            await interaction.response.send_message("La file d'attente est vide.", ephemeral=True)
            return

        queue_list = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(self.music_queue[guild_id])])
        await interaction.response.send_message(f"**File d'attente :**\n{queue_list}", ephemeral=True)

    @app_commands.command(name="pause", description="Met en pause la musique.")
    async def pause(self, interaction: discord.Interaction):
        voice_client = self.voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("Musique mise en pause ⏸️", ephemeral=True)
        else:
            await interaction.response.send_message("Aucune musique n'est en cours de lecture.", ephemeral=True)

    @app_commands.command(name="resume", description="Reprend la musique en pause.")
    async def resume(self, interaction: discord.Interaction):
        voice_client = self.voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("Musique reprise ▶️", ephemeral=True)
        else:
            await interaction.response.send_message("Aucune musique n'est en pause.", ephemeral=True)

    def _after_play(self, error, guild_id):
        """Fonction appelée après la lecture de la musique."""
        if error:
            print(f"Erreur pendant la lecture : {error}")
        # Lance la musique suivante dans la file d'attente
        asyncio.run(self.play_next(guild_id))

async def setup(bot):
    await bot.add_cog(Music(bot))
