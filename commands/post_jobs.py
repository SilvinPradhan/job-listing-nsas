import discord
from discord.ext import commands, tasks
from cogs.jobs import fetch_adzuna_jobs, format_jobs
from cogs.utils import split_message

class PostJobsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.post_jobs.start()
        
    # Task to automatically post new job listings every 6 hours and quotes   
    @tasks.loop(hours=72)
    async def post_jobs(self):
        await self.bot.wait_until_ready()
        JOB_POSTING_CHANNEL_ID = 1017817516342513704
        channel = self.bot.get_channel(JOB_POSTING_CHANNEL_ID)

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
            
async def setup(bot):
    await bot.add_cog(PostJobsCommands(bot))