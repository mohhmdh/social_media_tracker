import asyncio
import discord
from discord.ext import commands
import random

# Import the Facebook function
from fb_post import post_facebook ,post_image_to_facebook , post_video_to_facebook


intents = discord.Intents.all() #tells the Discord API what events the bot will receive (messages, members, reactions, presences, etc.).

with open(".env", "r") as file:
    TOKEN = file.readline().strip()


client = commands.Bot(command_prefix='.', intents=intents) #set the bot with command prefix and permissions

@client.event #get command
async def on_ready():
    print(f'{client.user} has logged in')

@client.command()
async def ping(ctx):
    #send msg to same channel
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')

@client.command()
async def quote(ctx):
    #reads all lines from quotes.txt into a list where each list element is a line
    responses = open('quotes.txt').read().splitlines()
    #picks one
    response = random.choice(responses)
    await ctx.send(response)

@client.command()
async def thnx(ctx):
    await ctx.send(f'No problem {ctx.author.name}!')

@client.command()
async def clear(ctx, amount: int = 5):#default = 5
    #built in function
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'Deleted {len(deleted)} messages!', delete_after=5)

@client.command()
async def gn(ctx):
    await ctx.send(f'You too ')

@client.command()
#capture the rest of the command input into message”
# (so .postfb hello world → message="hello world")
# . This allows multi-word messages , just after the command
#none is default
async def postfb(ctx, *, message: str = None):

    if not message:
        await ctx.send(" Format of the command: `.postfb <your message>`")#if no message supplied
        return

    await ctx.send("Posting to Facebook...")

    try:

      #  result = post_facebook(message)  # Big problem , take time (facebook while posting)unlike the bot
    # we use another worker thread ( tasks can run in parallel (other commands ))

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, post_facebook, message)
#we get id of the post ->done
        if isinstance(result, dict) and "id" in result:
            await ctx.send(f"Successfully posted to Facebook!")
        else:
            await ctx.send(f"Error: {result}")
 #other           
    except Exception as e:
        await ctx.send(f" Unexpected error: {e}")



@client.command()
async def postimg(ctx, *, caption: str = ""):
    if len(ctx.message.attachments) == 0:
        return await ctx.send(" Please attach an image with the command!")

    await ctx.send("Uploading to Facebook...")

    attachment = ctx.message.attachments[0]
    image_path = f"./{attachment.filename}"
    await attachment.save(image_path)

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, post_image_to_facebook, image_path, caption)

    if isinstance(result, dict) and "post_id" in result or "id" in result:
        await ctx.send(f" Image posted successfully!")
    else:
        await ctx.send(f" Error posting image: {result}")




@client.command()
async def postvideo(ctx, *, caption: str = ""):
    if len(ctx.message.attachments) == 0:
        return await ctx.send("Please attach a video with the command")

    await ctx.send("Uploading ")

    attachment = ctx.message.attachments[0]
    video_path = f"./{attachment.filename}"
    await attachment.save(video_path)

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, post_video_to_facebook, video_path, caption)
    if isinstance(result, dict) and "id" in result:
        await ctx.send(f"Video posted successfully")
    else:
        await ctx.send(f" Error : {result}")

client.run(TOKEN) #token of the bot , to contact it to the server (while creating it )