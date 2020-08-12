import random
import os
from typing import List

import discord
from discord.ext import commands
from discord.ext.commands import Bot

TOKEN = 'NzQyODg1ODY1NjE2ODM0Njcy.XzMoYA.7sXtZbYQZeLfazUxytX1598Mljo'
bot = commands.Bot(command_prefix='>')
client = discord.Client()

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(name='blade', help='Blade Runner é o filme favorito do meu criador, irônico não?')
async def blade_runner(ctx):
    blade_runner_quotes = [
        'Quite an experience to live in fear, isn t it? That s what it is to be a slave.',

        (
            'Replicants are like any other machine, are either a benefit or a hazard. If they are a benefit its not my '
            'problem.'
        ),
        'Its too bad she wont live, but then again who does?',
        (

            'Ive seen things you people wouldnt believe.Attack ships on fire off the shoulder of Orion. '
            'I watched c-beams glitter in the dark near the Tannhuser Gate.All those moments will be lost in time, '
            'like tears in rain. Time to die'
        ),

    ]
    response = random.choice(blade_runner_quotes)
    await ctx.send(response)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')



bot.run(TOKEN)
