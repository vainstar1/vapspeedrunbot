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

    if "speedrun" in message.content.lower():
        if current_time - last_used >= cooldown_time:
            last_used = current_time
            await message.reply(file=discord.File('speedrun.gif'))
        else:
            remaining_time = int(cooldown_time - (current_time - last_used))
            print("on cooldown gangy wangy")

    await bot.process_commands(message)

bot.run(TOKEN)
