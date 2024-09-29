import discord
from discord.ext import commands
from cogs.misc import fetchQuotesApi
from apscheduler.triggers.cron import CronTrigger

class MotivationalQuotesCommands(commands.Cog):
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler
        self.schedule_quote()

    def schedule_quote(self):
        #Run the function everyday at 8:30 Am 
        self.scheduler.add_job(self.get_quotes, CronTrigger(hour=8, minute=30))

    async def get_quotes(self):
        JOB_POSTING_CHANNEL_ID = 1017817516342513704
        channel = self.bot.get_channel(JOB_POSTING_CHANNEL_ID)
        if channel:
            apiUrl = 'https://zenquotes.io/api/quotes/'
            data = await fetchQuotesApi(apiUrl)
            mlist = []
            if data:
                # Data is a long list with each value of a dictionary. Taking only one element
                data = data[0]
                # Dict's first two elements are placed into a list to send it.
                for x in data.values():
                    mlist.append(x)
                try:
                    await channel.send(f" \"{mlist[0]}\"- {mlist[1]} ")
                    
                except discord.errors.HTTPException as e:
                    print(f"Failed to send data: {e}")
            else:
                await channel.send("Failed to fetch motivational quotes.")

async def setup(bot, scheduler):
    await bot.add_cog(MotivationalQuotesCommands(bot, scheduler))
