from io import BytesIO

import discord
from discord import Message
from discord.ext import commands
from PIL import Image

from main import main

config = {
    'token': 'MTIyODMxMzMyMDI4NTc5ODQzMg.GJM4MK.i9K966PPAf2nLb2FfH0hWOx_2ud4O5ZooIbtCI',
    'prefix': '/',
}

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)


@bot.event
async def on_message(message: Message):
    if message.author != bot.user:
        print(message.content)
        await message.reply(f"Received your message: {message.content}")


@bot.event
async def on_message(message: Message):
    if message.author != bot.user and message.attachments:
        for attachment in message.attachments:
            image_bytes = await attachment.read()
            image = Image.open(BytesIO(image_bytes))
            result_image = main(image)
            image_io = BytesIO()
            result_image.save(image_io, format='PNG')
            image_io.seek(0)

            await message.channel.send(file=discord.File(image_io, filename=attachment.filename))


bot.run(config['token'])
