import traceback
import discord
from discord import app_commands
from discord.ext import commands
from cogs.histogram import fetch_salary_histogram, plot_salary_histogram
from cogs.utils.us_states import US_STATES

class SalaryHistogramCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Slash command to generate and display salary histogram
    @app_commands.command(
        name="salary_histogram",
        description="Fetch and display salary distribution for a job title in a specific state"
    )
    @app_commands.describe(job_title="Enter the job title", state="Enter the state abbreviation (e.g., TX, CA)")
    async def salary_histogram(self, interaction: discord.Interaction, job_title: str, state: str):
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
    
async def setup(bot):
    await bot.add_cog(SalaryHistogramCommands(bot))        