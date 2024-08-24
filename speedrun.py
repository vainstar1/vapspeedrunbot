import discord
import os
import time
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = 745762346479386686 

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

@bot.tree.command(name='secret')
async def secret_command(interaction: discord.Interaction, new_cooldown: int = None):
    global cooldown_time
    if interaction.user.id == OWNER_ID:
        if new_cooldown is not None:
            cooldown_time = new_cooldown
            await interaction.response.send_message(f"Cooldown time updated to {cooldown_time} seconds.", ephemeral=True)
        else:
            await interaction.response.send_message("specify your cooldown bro", ephemeral=True)
    else:
        await interaction.response.send_message("Only Odd can use this command.", ephemeral=True)

bot.run(TOKEN)
