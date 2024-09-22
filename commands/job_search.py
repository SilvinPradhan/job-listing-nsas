import discord
from discord import app_commands
from discord.ext import commands
import requests
from cogs.jobs import fetch_adzuna_jobs, format_jobs
from cogs.utils import split_message, US_STATES, JOB_FIELDS
from discord.ext.commands import CommandOnCooldown

class JobSearchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(
        name="job_search_by_keywords",
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
    
    # Job Search using keywords and optional filters
    async def job_search_by_keywords(self, interaction: discord.Interaction, keywords: str, location: str, salary_min: int = 0, company: str = "", page: int = 1, days_limit: int = 30):
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
    @app_commands.command(
        name="job_search_internships",
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
    async def job_search_internships(self, interaction: discord.Interaction,
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
            
async def setup(bot):
    await bot.add_cog(JobSearchCommands(bot))