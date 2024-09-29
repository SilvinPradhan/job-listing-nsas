from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize the scheduler
scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is now online!")
    await bot.tree.sync()

# Load all command cogs from commands folder
async def load_commands():
    await bot.load_extension("commands.job_search")
    await bot.load_extension("commands.salary_histogram")
    await bot.load_extension("commands.fetch_jobs_excel")
    await bot.load_extension("commands.post_jobs")

    # Manually add the motivational quote cog with the scheduler
    from commands.motivational_quote import MotivationalQuotesCommands
    await bot.add_cog(MotivationalQuotesCommands(bot, scheduler))

async def main():
    await load_commands()

    # Start the scheduler
    scheduler.start()
    
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
