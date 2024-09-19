import discord
from discord.ext import commands, tasks
from discord import app_commands

from dotenv import load_dotenv
import os
from cogs import fetch_adzuna_jobs, split_message, format_jobs, US_STATES, JOB_FIELDS
from discord.ext.commands import CommandOnCooldown

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
JOB_POSTING_CHANNEL_ID = 1285754369689522319

# Initialize bot with the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Define the bot and command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash command to fetch job listings by user request with additional filters
@bot.tree.command(
    name="job",
    description="Fetch the latest jobs or internships for a specific field in a US state"
)
@app_commands.describe(
    field="Select a job field",
    state="Enter a valid US state code (e.g., LA for Louisiana)",
    salary_min="Optional: Set a minimum salary (e.g., 50000)",
    company="Optional: Search for jobs by a specific company",
    days_limit="Optional: Limit jobs to those posted within the last X days (default: 30)",
    page="Optional: Specify a page for pagination (default: 1)"
)
@app_commands.choices(field=JOB_FIELDS)
@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)  # Rate limit: 1 use per 30 seconds per user
async def job(interaction: discord.Interaction,
              field: app_commands.Choice[str], 
              state: str, 
              salary_min: int = 0, 
              company: str = "", 
              days_limit: int = 30, 
              page: int = 1):
    try:
        state_code = state.upper()
        if state_code not in US_STATES:
            await interaction.response.send_message(
                "Invalid US state code. Please use a valid two-letter state code (e.g., LA, TX, NY)."
            )
            return

        search_term = field.value + " job"
        jobs = fetch_adzuna_jobs(
            search_term, 
            location=US_STATES[state_code], 
            salary_min=salary_min, 
            company=company, 
            days_limit=days_limit, 
            page=page
        )
        
        job_listings = format_jobs(jobs)
        if job_listings:
            chunks = split_message(job_listings)
            await interaction.response.send_message(chunks[0])
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk)
        else:
            await interaction.response.send_message(
                f"No job listings found for {field.name} in {US_STATES[state_code]}."
            )
    except CommandOnCooldown as e:
        await interaction.response.send_message(
            f"You're doing that too often! Try again in {e.retry_after:.2f} seconds.",
            ephemeral=True
        )


# Task to automatically post new job listings every 6 hours
@tasks.loop(hours=6)
async def post_jobs():
    await bot.wait_until_ready()

    channel = bot.get_channel(JOB_POSTING_CHANNEL_ID)

    if channel is None:
        print(f"Error: Channel with ID {JOB_POSTING_CHANNEL_ID} not found.")
        return

    # Fetch jobs for Computer Science in Louisiana (Default)
    cs_jobs = fetch_adzuna_jobs('computer science job', location='Louisiana')
    if cs_jobs:
        await channel.send("**Latest Computer Science Jobs in Louisiana:**")
        job_listings_cs = format_jobs(cs_jobs)
        chunks_cs = split_message(job_listings_cs)
        for chunk in chunks_cs:
            await channel.send(chunk)

    # Fetch jobs for Biology in Louisiana (Default)
    bio_jobs = fetch_adzuna_jobs('biology job', location='Louisiana')
    if bio_jobs:
        await channel.send("**Latest Biology Jobs in Louisiana:**")
        job_listings_bio = format_jobs(bio_jobs)
        chunks_bio = split_message(job_listings_bio)
        for chunk in chunks_bio:
            await channel.send(chunk)


@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is now online!")
    post_jobs.start()
    await bot.tree.sync()

bot.run(DISCORD_BOT_TOKEN)
