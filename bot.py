import discord
from discord.ext import commands
from keep_alive import keep_alive
import aiohttp
import os

# Setup Intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix=',', intents=intents)

# --- CONFIGURATION ---
OWNER_ROLE_ID = 1458370959537999934
BAD_WORDS = ["word1", "word2"] # Add your list here!

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 1. STOP LARGE TEXT (# HEADERS)
    if message.content.startswith("#"):
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, big text is not allowed!", delete_after=5)
        return

    # 2. STOP OWNER ROLE PINGS
    if any(role.id == OWNER_ROLE_ID for role in message.role_mentions):
        await message.delete()
        await message.channel.send(f"❌ {message.author.mention}, don't ping the Owner!", delete_after=5)
        return

    # 3. BAD WORD FILTER
    msg_content = message.content.lower()
    if any(word in msg_content for word in BAD_WORDS):
        await message.delete()
        await message.channel.send(f"🚫 {message.author.mention}, watch your language!", delete_after=3)
        return

    await bot.process_commands(message)

# --- MEME COMMAND ---
@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as response:
            data = await response.json()
            embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color.random())
            embed.set_image(url=data['url'])
            embed.set_footer(text=f"Meme from r/{data['subreddit']}")
            await ctx.send(embed=embed)

keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
