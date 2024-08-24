import discord
import os
import time
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

cooldown_time = 1800 
last_used = 0 

trigger_phrases = ["speedrun", "speedruns", "speedrunning"]  

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.event
async def on_message(message):
    global last_used
    current_time = time.time()

    if any(phrase in message.content.lower() for phrase in trigger_phrases):
        if current_time - last_used >= cooldown_time:
            last_used = current_time
            await message.reply(file=discord.File('speedrun.gif'))
        else:
            remaining_time = int(cooldown_time - (current_time - last_used))
            print(f"on cooldown for {remaining_time} seconds")

    await bot.process_commands(message)

bot.run(TOKEN)
