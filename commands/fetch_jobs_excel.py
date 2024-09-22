import traceback
import discord
from discord import app_commands
from discord.ext import commands
from cogs.excel import create_excel_file
from cogs.jobs import fetch_jobs_from_adzuna

class FetchJobsExcelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to fetch and export jobs to Excel
    @app_commands.command(
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
        self,
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
    
async def setup(bot):
    await bot.add_cog(FetchJobsExcelCommands(bot))