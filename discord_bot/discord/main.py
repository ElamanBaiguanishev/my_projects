import discord
from discord.ext import commands

config = {
    'token': 'MTE0MTAzOTkyMjEwNzY2MjQzNg.GHwXke.EO_0jUp5o-NUYVhuuVZtxQsm0emFmCcCdly2eA',
    'prefix': '!',
}

intents = discord.Intents.default()
intents.message_content = True  # Enable the required intent

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    print(message)


bot.run(config['token'])
