import discord
import os
from discord.ext import commands
from config import TOKEN

class Soushi(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def load_files(self, path: str):
        for file_name in os.listdir(f"./{path}"):
            if file_name.endswith(".py"):
                cog = f"{path.replace('/', '.')}.{file_name[:-3]}"
                try:
                    await self.load_extension(cog)
                    print(f"Loaded {cog}")
                except Exception as e:
                    print(f"Failed to load {cog}: {e}")

    async def setup_hook(self):
        await self.load_files("modules/moderation")
        await self.load_files("modules/basic")
        await self.load_files("modules/fun")
        await self.load_files("modules/skid")
        await self.load_files("events")
        await self.tree.sync()


def main():
    intents = discord.Intents.all()
    bot = Soushi(command_prefix="/", intents=intents)
    bot.run(TOKEN)

if __name__ == "__main__":
    main()