import discord
from discord.ext import commands, tasks
from cogs.misc import fetchQuotesApi

class MotivationalQuotesCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_quotes.start()

    @tasks.loop(hours=24)
    async def get_quotes(self):
        JOB_POSTING_CHANNEL_ID = 1017817516342513704
        channel = self.bot.get_channel(JOB_POSTING_CHANNEL_ID)
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

async def setup(bot):
    await bot.add_cog(MotivationalQuotesCommands(bot))