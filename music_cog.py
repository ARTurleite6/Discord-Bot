import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.queue = []
        self.vc = None
        self.is_playing = False
        self.is_paused = False

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist' : 'True'}
        self.FFMPEGPCMAUDIO = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    def search_music(self, url):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)['url']
                return info
            except Exception:
                print("Videos not found")
                return False

    @commands.command(name="join", aliases=["j"], help="Comando que faz o bot entrar no canal")
    async def join(self, ctx: commands.Context):
        if ctx.author.voice:
            self.vc = await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Não estas num canad de voz")

    @commands.command(name="leave", aliases=["l"], help="Comando para o bot sair do canal de voz")
    async def leave(self, ctx: commands.Context):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Não estou num canal de voz")

    def play_next(self):
        if self.vc is None:
            print("Bot is not connected")

        if len(self.queue) > 0:
            song = self.search_music(self.queue.index(0))
            self.queue.pop(0)
            self.is_playing = True
            self.is_paused = False

            self.vc.play(discord.FFmpegPCMAudio(song, **self.FFMPEGPCMAUDIO), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            self.is_paused = False
            print("Não existem musicas na fila de espera")

    @commands.command(name="pause", aliases=["pa"], help="Comando que poe em as musicas em pausa")
    async def pause(self, ctx: commands.Context):
        if self.vc is None:
            await ctx.send("Não estou em nenhum canal de voz")
        elif not self.is_playing:
            await ctx.send("Não estou a tocar nenhuma musica agora")
        else:
            self.is_paused = True
            self.is_playing = False
            self.vc.pause()

    @commands.command(name="stop", aliases=["s"], help="Comando que para de tocar musicas")
    async def stop(self, ctx: commands.Context):
        if self.vc is None:
            await ctx.send("Não estou em nenhum canal de voz")
        elif self.is_playing or self.is_paused:
            self.is_playing = False
            self.is_paused = False
            self.vc.stop()

    @commands.command(name="resume", aliases=["r"], help="Comando que poe a tocar outra vez as musicas")
    async def resume(self, ctx: commands.Context):
        if self.vc is None:
            await ctx.send("Não estou em nenhum canal de voz")
        elif self.is_playing:
            await ctx.send("Já estou a tocar musicas filho")
        elif not self.is_playing:
            await ctx.send("Não estou a tocar nenhuma musica filho")
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="play", aliases=["p"], help="Comando que toca uma musica passada")
    async def play(self, ctx: commands.Context, song_url):
        if self.vc is None:
            await self.join(ctx)
        if song_url is not None:
            song = self.search_music(song_url)
            if song:
                self.vc.play(discord.FFmpegPCMAudio(song, **self.FFMPEGPCMAUDIO), after=lambda e: self.play_next())
                self.is_playing = True

    @commands.command(name="addqueue", aliases=["aq"], help="Adiciona uma musica à fila de espera")
    async def add_queue(self, ctx: commands.Context, url):
        if ctx.author.voice:
            self.queue.append(url)
        else:
            await ctx.send("You need to be in a voice channel")

    @commands.command(name="queue", aliases=["q"], help="Mostra a fila de espera atual")
    async def queue(self, ctx: commands.Context):
        result = ""
        priority = 1
        for music in self.queue:
            result += str(priority) + " " + music[0] + "\n"
            priority += 1
        if len(result) == 0:
            result = "Não existem musicas na fila de espera"

        await ctx.send(result)
