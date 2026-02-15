import discord
from discord.ext import commands
from keep_alive import keep_alive
import aiohttp
import os

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix=',', intents=intents)

# --- CONFIGURATION ---
OWNER_ROLE_ID = 1458370959537999934
# Add all your bad words here (make them lowercase)
BAD_WORDS = ["fuck", "fick", "badword1"] 

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} is online!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    # 1. DELETE LARGE TEXT (#)
    if message.content.startswith("#"):
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, no big text!", delete_after=3)
        return

    # 2. DELETE OWNER PINGS
    if any(role.id == OWNER_ROLE_ID for role in message.role_mentions):
        await message.delete()
        await message.channel.send(f"❌ {message.author.mention}, don't ping the Owner!", delete_after=3)
        return

    # 3. DELETE BAD WORDS
    if any(word in msg for word in BAD_WORDS):
        await message.delete()
        await message.channel.send(f"🚫 {message.author.mention}, watch your language!", delete_after=3)
        return

    # CRITICAL: This line allows your commands (,meme, ,clear) to work!
    await bot.process_commands(message)

# --- MEME COMMAND ---
@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as response:
            data = await response.json()
            embed = discord.Embed(title=data['title'], color=discord.Color.random())
            embed.set_image(url=data['url'])
            await ctx.send(embed=embed)

# --- NEW CLEAR COMMAND ---
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Deletes the specified number of messages (default 5)."""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Cleared {amount} messages!", delete_after=3)

keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
