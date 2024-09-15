import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, voice_recv
import speech_recognition as sr
import asyncio
from typing import Optional
from tts import tts
from model import get_response
from shared import prompts_queue  # Import from the new shared module

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    voice_clients = {}
    play_lock = asyncio.Lock()
    current_prompt = None  # Track the currently processing prompt

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")

    @bot.tree.command(name="listen", description="Listen to vc")
    async def listen(interaction: discord.Interaction):
        class MySpeechRecognitionSink(voice_recv.extras.SpeechRecognitionSink):
            def __init__(self, bot, play_lock):
                super().__init__(process_cb=self.process_audio, text_cb=self.handle_text)
                self.bot = bot
                self.audio_file_path = "audio.wav"
                self.play_lock = play_lock
                self.is_playing_audio = False  # Track whether audio is being played

            def process_audio(self, recognizer: sr.Recognizer, audio: sr.AudioData, user: discord.User) -> Optional[str]:
                if self.is_playing_audio:
                    print("Currently playing audio. Ignoring speech input.")
                    return None  # Skip processing if playing audio

                try:
                    text = recognizer.recognize_google(audio)
                    return text
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    return None

            def handle_text(self, user: discord.User, text: Optional[str]) -> None:
                if text and not self.is_playing_audio:  # Check if audio is not being played
                    print(f"{user.display_name} said: {text}")
                    prompt = (user, text)
                    prompts_queue.append(prompt)  # Add to the queue
                    asyncio.run_coroutine_threadsafe(self.process_and_play_response(user, text), self.bot.loop)

            async def process_and_play_response(self, user: discord.User, text: str):
                async with self.play_lock:
                    nonlocal current_prompt

                    prompt = (user, text)
                    if prompt not in prompts_queue:
                        print("Prompt was deleted before processing. Skipping.")
                        return

                    current_prompt = prompt
                    response = get_response(f"{user.display_name}: {text}")
                    tts(response, self.audio_file_path)
                    await self.play_audio_file()

                    # After processing, remove the prompt from the queue
                    if current_prompt in prompts_queue:
                        prompts_queue.remove(current_prompt)
                    current_prompt = None  # Reset the current prompt

            async def play_audio_file(self):
                self.is_playing_audio = True  # Set playing state to True
                voice_client = discord.utils.get(self.bot.voice_clients, guild=self.bot.guilds[1])
                if voice_client and not voice_client.is_playing():
                    if os.path.exists(self.audio_file_path):
                        source = discord.FFmpegPCMAudio(self.audio_file_path)
                        voice_client.play(source)
                        while voice_client.is_playing():
                            await asyncio.sleep(1)
                        os.remove(self.audio_file_path)
                    else:
                        print("Error: Audio file not found.")
                else:
                    print("Error: Not connected to a voice channel or already playing audio.")
                
                self.is_playing_audio = False  # Reset playing state after audio finishes


        guild_id = interaction.guild.id
        if guild_id not in voice_clients:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
                sink = MySpeechRecognitionSink(bot, play_lock)
                vc.listen(sink)
                voice_clients[guild_id] = vc
                await interaction.response.send_message("Listening to the voice channel.")
            else:
                await interaction.response.send_message("You are not in a voice channel.")
        else:
            await interaction.response.send_message("Already listening in a voice channel.")

    @bot.tree.command(name="stop", description="Stop listening")
    async def stop(interaction: discord.Interaction):
        guild_id = interaction.guild.id
        if guild_id in voice_clients:
            vc = voice_clients[guild_id]
            await vc.disconnect()
            del voice_clients[guild_id]
            await interaction.response.send_message("Stopped listening and disconnected.")
        else:
            await interaction.response.send_message("Not currently listening to any voice channel.")

    bot.run(TOKEN)
