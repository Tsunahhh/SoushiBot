import discord
import os
from discord.ext import commands
from config import TOKEN

class Soushi(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_modules()

    def load_files(self, path: str):
        for file_name in os.listdir(f"./{path}"):
            if file_name.endswith(".py"):
                cog = f"cogs.{file_name[:-3]}"
                try:
                    self.load_extension(cog)
                    print(f"Loaded {cog}")
                except Exception as e:
                    print(f"Failed to load {cog}: {e}")

    def load_modules(self):
        self.load_files("modules/moderation")
        self.load_files("modules/basic")
        self.load_files("events")


def main():
    intents = discord.Intents.all()
    bot = Soushi(command_prefix="/", intents=intents)

    async def setup_hook():
        await bot.tree.sync()

    bot.setup_hook = setup_hook

    bot.run(TOKEN)


if __name__ == "__main__":
    main()



