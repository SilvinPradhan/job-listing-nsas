import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is now online!")
    await bot.tree.sync()
    
# Load all command cogs from commands folder
async def load_commands():
    await bot.load_extension("commands.job_search")
    await bot.load_extension("commands.motivational_quote")
    await bot.load_extension("commands.salary_histogram")
    await bot.load_extension("commands.fetch_jobs_excel")
    await bot.load_extension("commands.post_jobs")

async def main():
    await load_commands()
    
    try:
        await bot.start(DISCORD_BOT_TOKEN)
    except KeyboardInterrupt:
        print("Shutting down the bot...")
        await bot.close()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

# Launch the bot in an async-safe context
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot terminated by user.")
