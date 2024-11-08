import discord

bot = discord.Bot()

# create Slash Command group with bot.create_group
greetings = bot.create_group("greetings", "Greet people")


@greetings.command()
async def hello(ctx):
    await ctx.respond(f"Hello, {ctx.author}!")


@greetings.command()
async def bye(ctx):
    await ctx.respond(f"Bye, {ctx.author}!")


math = discord.SlashCommandGroup("math", "Math related commands")


@math.command()
async def add(ctx, num1: int, num2: int):
    sum = num1 + num2
    await ctx.respond(f"{num1} plus {num2} is {sum}.")


@math.command()
async def subtract(ctx, num1: int, num2: int):
    sum = num1 - num2
    await ctx.respond(f"{num1} minus {num2} is {sum}.")


# you'll have to manually add the manually created Slash Command group
bot.add_application_command(math)
print("Я СТАРТУЮ")
bot.run('MTIyODMxMzMyMDI4NTc5ODQzMg.GJM4MK.i9K966PPAf2nLb2FfH0hWOx_2ud4O5ZooIbtCI')
