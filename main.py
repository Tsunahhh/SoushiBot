import discord
import os
from discord.ext import commands
from config import TOKEN

class Soushi(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_moderation()

    def load_modules(self, path: str):
        for file_name in os.listdir(f"./modules/{path}"):
            if file_name.endswith(".py"):
                cog = f"cogs.{file_name[:-3]}"
                try:
                    self.load_extension(cog)
                    print(f"Loaded {cog}")
                except Exception as e:
                    print(f"Failed to load {cog}: {e}")

        async def on_ready(self):
            print(f"{self.user} is ready !")
                    

    def load_moderation(self):
        self.load_modules("moderation")


def main():
    intents = discord.Intents.all()
    bot = Soushi(command_prefix="/", intents=intents)

    async def setup_hook():
        await bot.tree.sync()

    bot.setup_hook = setup_hook

    bot.run(TOKEN)


if __name__ == "__main__":
    main()



