import discord
from discord.ext import commands
from music_cog import Music


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)
        self.add_commands()
        self.add_events()
        music_c = Music(self)
        self.add_cog(music_c)

    def add_events(self):
        @self.event
        async def on_ready():
            print(f"Connected {self.user}")

    def add_commands(self):
        @self.command()
        async def ping(ctx: commands.Context):
            await ctx.send("pong")

        @self.command()
        async def about(ctx: commands.Context):
            await ctx.send("Ola, sou o Joaquim Bot, familiar do Tomas")


def main():
    bot = Bot()
    bot.run('OTg0NTcwMzcxMTYyMzc0MTg2.GEoZ4X.V4mPXIb46uufP7-obt_7SawVm5I5tmSOMy_ZP4')


if __name__ == "__main__":
    main()
