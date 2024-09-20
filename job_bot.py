import discord
import requests
from discord.ext import commands, tasks
from discord import app_commands, channel
from dotenv import load_dotenv
import os
import traceback
from cogs.jobs import fetch_adzuna_jobs, format_jobs, fetch_jobs_from_adzuna
from cogs.utils import split_message, US_STATES, JOB_FIELDS
from cogs.misc import fetchQuotesApi
from cogs.excel import create_excel_file
from cogs.histogram import fetch_salary_histogram, plot_salary_histogram
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
    location="Enter a US state abbreviation (e.g., TX for Texas, LA for Louisiana)",
    salary_min="Enter the minimum salary (optional)",
    company="Enter the company name (optional)",
    page="Enter the page number for pagination (default is 1)",
    days_limit="Enter the number of days to limit job postings (optional)"
)
async def search_jobs(interaction: discord.Interaction, keywords: str, location: str, salary_min: int = 0, company: str = "", page: int = 1, days_limit: int = 30):
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
        jobs = fetch_adzuna_jobs(keywords, full_location, salary_min=salary_min, company=company, page=page, days_limit=days_limit)

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
    state="Enter a valid US state code (e.g., LA for Louisiana)",
    salary_min="Enter the minimum salary (optional)",
    company="Enter the company name (optional)",
    page="Enter the page number for pagination (default is 1)",
    days_limit="Enter the number of days to limit job postings (optional)"
)
@app_commands.choices(field=JOB_FIELDS)
@commands.cooldown(
    rate=1, per=30,
    type=commands.BucketType.user)  # Rate limit: 1 use per 30 seconds per user
async def job(interaction: discord.Interaction,
              field: app_commands.Choice[str], state: str, salary_min: int = 0, company: str = "", page: int = 1, days_limit: int = 30):
    try:
        state_code = state.upper()
        if state_code not in US_STATES:
            await interaction.response.send_message(
                "Invalid US state code. Please use a valid two-letter state code (e.g., LA, TX, NY)."
            )
            return
        search_term = field.value + " internship"
        jobs = fetch_adzuna_jobs(search_term, location=US_STATES[state_code], salary_min=salary_min, company=company, page=page, days_limit=days_limit)
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
        mlist = []
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
            
    # Fetch additional fields (if needed) -- discord server timesout (Possible future )
    # for field in JOB_FIELDS:
    #     field_jobs = fetch_adzuna_jobs(f'{field} internship', location='Louisiana')
    #     if field_jobs:
    #         await channel.send(f"**Latest {field.capitalize()} Internships in Louisiana:**")
    #         job_listings_field = format_jobs(field_jobs)
    #         chunks_field = split_message(job_listings_field)
    #         for chunk in chunks_field:
    #             await channel.send(chunk)

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

        state_code = state.upper()
        if state_code not in US_STATES:
            await interaction.followup.send("Invalid state abbreviation. Please use valid two-letter US state codes (e.g., TX, CA).", ephemeral=True)
            return

        full_state_name = US_STATES[state_code]

        histogram_data = fetch_salary_histogram(job_title, full_state_name)

        if not histogram_data:
            await interaction.followup.send(f"No salary histogram data found for {job_title} in {full_state_name}.", ephemeral=True)
            return

        histogram_image = plot_salary_histogram(histogram_data)

        if histogram_image is None:
            await interaction.followup.send("Failed to generate the salary histogram.", ephemeral=True)
            return

        # Send the histogram plot as an image
        await interaction.followup.send(file=discord.File(histogram_image, 'salary_histogram.png'))

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

# Command to fetch and export jobs to Excel
@bot.tree.command(
    name="fetch_jobs_excel", 
    description="Fetch top 10 latest jobs and export them as an Excel file"
)
@app_commands.describe(
    title="Enter job title or keyword",
    job_type="Specify job type: full_time, part_time, permanent, or contract",
    state="Enter the state abbreviation (e.g., CA for California)",
    city="Enter the city name"
)
async def fetch_jobs_excel(
    interaction: discord.Interaction, 
    title: str, 
    job_type: str, 
    state: str, 
    city: str
):
    try:
        await interaction.response.defer()

        jobs_data = await fetch_jobs_from_adzuna(title, job_type, state, city)
        if not jobs_data:
            await interaction.followup.send("Failed to fetch job data.", ephemeral=True)
            return

        excel_file = create_excel_file(jobs_data)
        
        formatted_title = title.replace(" ", "_").lower()
        formatted_job_type = job_type.lower()
        formatted_city = city.replace(" ", "_").lower()
        formatted_state = state.upper()
        
        file_name = f"top_10_latest_{formatted_title}_{formatted_job_type}_in_{formatted_city}_{formatted_state}.xlsx"

        # Send the file as an attachment
        await interaction.followup.send(file=discord.File(excel_file, file_name))

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error: {e}")
        print(f"Traceback:\n{error_trace}")

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is now online!")
    # post_jobs.start()
    await getQuotes()
    await bot.tree.sync()

bot.run(DISCORD_BOT_TOKEN)
