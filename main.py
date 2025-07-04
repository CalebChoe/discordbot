import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import webserver

secret_role = 'test role'

communication_crap = [['hi', 'hey buddy'], ['hello', 'hey buddy'],
                      ["what's up", 'nothing much']]

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'welcome {bot.user.name}')

@bot.event
async def on_member_join(member):
    await member.send(f'welcome {member.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    badwordslist = ['ass', 'shit', 'fuck', 'bitch'] # curse words, censored
    for i in badwordslist:
        if i in message.content.lower():
            # enable line below for filter delete
            # await message.delete()
            await message.channel.send(f'{message.author.mention} just said {i}!! '
                                       f'\n Shun them!')
    if 'kanye' in message.content.lower():
        for i in communication_crap:
            print(i)
            if i[0] in message.content.lower():
                await message.channel.send(i[1])

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f'hi {ctx.author.mention}')

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f'{ctx.author.mention} has {secret_role} now')
    else:
        await ctx.send("that doesn't work, role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f'{ctx.author.mention} has had {secret_role} removed')
    else:
        await ctx.send("that doesn't work, role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f'did you just say "{msg}"')

@bot.command()
async def reply(ctx):
    poss = ['hmmm', 'yeezy season approaching', 'im a genius', 'aldis',
            'im too lazy to think of something to say', 'i love kanye',
            'kanye mentioned?', 'kanye.', 'i forgot', 'wheres @cronchiboi',
            'you should equip the SUIT tag if you have not done so yet',
            'kanye!', 'kanye?', 'i miss the old kanye']
    var = random.randint(1, len(poss))
    r = poss[var]
    await ctx.reply(r)

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title='poll thing', description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("✅")
    await poll_message.add_reaction("❌")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send('cool secret message ping @cronchiboi for a cookie')

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('loser')

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
