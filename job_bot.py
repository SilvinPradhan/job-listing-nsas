import discord
import requests
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import os
import traceback
from cogs import fetch_adzuna_jobs, split_message, format_jobs, US_STATES, JOB_FIELDS, fetchQuotesApi, fetch_salary_histogram, plot_salary_histogram
from discord.ext.commands import CommandOnCooldown

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
JOB_POSTING_CHANNEL_ID = 1285276393235550231

# Initialize bot with the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Define the bot and command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(
    name="search_jobs",
    description="Search for jobs by custom keywords and location (state abbreviation)"
)
@app_commands.describe(
    keywords="Enter the job title or keywords",
    location="Enter a US state abbreviation (e.g., TX for Texas, LA for Louisiana)"
)
async def search_jobs(interaction: discord.Interaction, keywords: str, location: str):
    try:
        # Check if keywords or location is empty
        if not keywords.strip():
            await interaction.response.send_message("Please provide valid keywords for the job search.", ephemeral=True)
            return
        if not location.strip():
            await interaction.response.send_message("Please provide a valid location for the job search.", ephemeral=True)
            return

        # Convert the location (state abbreviation) to full state name
        state_code = location.upper()
        if state_code not in US_STATES:
            await interaction.response.send_message(
                "Invalid US state code. Please use a valid two-letter state code (e.g., LA, TX, NY).",
                ephemeral=True
            )
            return

        # Use the full state name in the search
        full_location = US_STATES[state_code]

        # Fetch jobs using the helper function
        jobs = fetch_adzuna_jobs(keywords, full_location)

        # If the response is empty or no jobs found
        if not jobs:
            await interaction.response.send_message(
                f"No job listings found for '{keywords}' in '{full_location}'. Please try different keywords or location.",
                ephemeral=True
            )
            return

        # Format job listings and split them into chunks for Discord message limits
        job_listings = format_jobs(jobs)
        if job_listings:
            chunks = split_message(job_listings)
            await interaction.response.send_message(chunks[0])  # Send the first chunk
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk)  # Send subsequent chunks
        else:
            await interaction.response.send_message(
                f"No job listings found for '{keywords}' in '{full_location}'.",
                ephemeral=True
            )

    except requests.exceptions.RequestException as e:
        # Handle connection errors (e.g., API unreachable)
        await interaction.response.send_message(
            "Failed to retrieve job listings due to a connection issue. Please try again later.",
            ephemeral=True
        )
        print(f"RequestException: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        await interaction.response.send_message(
            "An unexpected error occurred while processing your request. Please try again later.",
            ephemeral=True
        )
        print(f"Unexpected error: {e}")


# Slash command to fetch job listings by user request with rate limiting
@bot.tree.command(
    name="job",
    description=
    "Fetch the latest internships for a specific field in a US state")
@app_commands.describe(
    field="Select a job field",
    state="Enter a valid US state code (e.g., LA for Louisiana)")
@app_commands.choices(field=JOB_FIELDS)
@commands.cooldown(
    rate=1, per=30,
    type=commands.BucketType.user)  # Rate limit: 1 use per 30 seconds per user
async def job(interaction: discord.Interaction,
              field: app_commands.Choice[str], state: str):
    try:
        state_code = state.upper()
        if state_code not in US_STATES:
            await interaction.response.send_message(
                "Invalid US state code. Please use a valid two-letter state code (e.g., LA, TX, NY)."
            )
            return
        search_term = field.value + " internship"
        jobs = fetch_adzuna_jobs(search_term, location=US_STATES[state_code])
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
            ephemeral=True)


@tasks.loop(hours=24)
async def getQuotes():
    channel = bot.get_channel(JOB_POSTING_CHANNEL_ID)
    if channel:
        apiUrl = 'https://zenquotes.io/api/quotes/'
        data = await fetchQuotesApi(apiUrl)
        mlist =[]
        if data:
            # Data is long list with each value of dictionary. taking only one element
            data = data[0]
            # Dict's first two elements is placed into list to send it.
            for x in data.values():
                mlist.append(x)
            try:
                await channel.send(f" \"{mlist[0]}\"- {mlist[1]} ")
                
            except discord.errors.HTTPException as e:
                print(f"Failed to send data: {e}")
        else:
            await channel.send("Failed to fetch motivational quotes.")


# Task to automatically post new job listings every 6 hours and quotes   
@tasks.loop(hours=6)
async def post_jobs():
    await bot.wait_until_ready()

    channel = bot.get_channel(JOB_POSTING_CHANNEL_ID)

    if channel is None:
        print(f"Error: Channel with ID {JOB_POSTING_CHANNEL_ID} not found.")
        return

    # Fetch jobs for Computer Science in Louisiana (Default)
    cs_jobs = fetch_adzuna_jobs('computer science internship', location='Louisiana')
    if cs_jobs:
        await channel.send(
            "**Latest Computer Science Internships in Louisiana:**")
        job_listings_cs = format_jobs(cs_jobs)
        chunks_cs = split_message(job_listings_cs)
        for chunk in chunks_cs:
            await channel.send(chunk)

    # Fetch jobs for Biology in Louisiana (Default)
    bio_jobs = fetch_adzuna_jobs('biology internship', location='Louisiana')
    if bio_jobs:
        await channel.send("**Latest Biology Internships in Louisiana:**")
        job_listings_bio = format_jobs(bio_jobs)
        chunks_bio = split_message(job_listings_bio)
        for chunk in chunks_bio:
            await channel.send(chunk)

# Slash command to generate and display salary histogram
@bot.tree.command(
    name="salary_histogram",
    description="Fetch and display salary distribution for a job title in a specific state"
)
@app_commands.describe(job_title="Enter the job title", state="Enter the state abbreviation (e.g., TX, CA)")
async def salary_histogram(interaction: discord.Interaction, job_title: str, state: str):
    try:
        # Defer the response immediately to avoid timeout issues
        await interaction.response.defer()

        # Convert the state abbreviation to the full state name
        state_code = state.upper()
        if state_code not in US_STATES:
            await interaction.followup.send("Invalid state abbreviation. Please use valid two-letter US state codes (e.g., TX, CA).", ephemeral=True)
            return

        full_state_name = US_STATES[state_code]  # Convert abbreviation to full state name

        # Fetch salary histogram data from Adzuna API
        histogram_data = fetch_salary_histogram(job_title, full_state_name)

        if not histogram_data:
            await interaction.followup.send(f"No salary histogram data found for {job_title} in {full_state_name}.", ephemeral=True)
            return

        # Generate the histogram plot
        histogram_image = plot_salary_histogram(histogram_data)

        # Check if the plot was generated successfully
        if histogram_image is None:
            await interaction.followup.send("Failed to generate the salary histogram.", ephemeral=True)
            return

        # Send the histogram plot as an image
        await interaction.followup.send(file=discord.File(histogram_image, 'salary_histogram.png'))

    except Exception as e:
        # Send the error as a follow-up message (since interaction has already been deferred)
        await interaction.followup.send("An error occurred while fetching or plotting the salary histogram.", ephemeral=True)
        print(f"Error: {e}")
        traceback.print_exc()

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is now online!")
    # post_jobs.start()
    await getQuotes()
    await bot.tree.sync()

bot.run(DISCORD_BOT_TOKEN)
