import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

# Setup Intents (Permissions)
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix=',', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 1. STOP LARGE TEXT (# HEADERS)
    if message.content.startswith("#"):
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, big text is not allowed here!", delete_after=5)
        return

    # 2. STOP OWNER ROLE PINGS
    # Replace 123456789012345678 with your actual Owner Role ID
    OWNER_ROLE_ID = 123456789012345678 
    
    if any(role.id == OWNER_ROLE_ID for role in message.role_mentions):
        await message.delete()
        await message.channel.send(f"❌ {message.author.mention}, don't ping the Owner!", delete_after=5)
        return

    await bot.process_commands(message)

# Start the web server trick
keep_alive()

# Use an Environment Variable for the token (Better for security)
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
