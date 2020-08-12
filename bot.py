import os
import fnmatch
import discord
from dotenv import load_dotenv
import numpy as np
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='%')


def read_rule(*rule):
    dir = ''
    for word in rule:
        dir = dir + '/' + word
        print(dir)
    with open(f'rules{dir}.txt', mode='r') as file:
        answer = file.read()
    return answer


@bot.event  # Connection
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='rule', help='Quick guide for the game rules') # Rule Library
async def get_rule(ctx, subject='', *especification):
    if subject == '':
        response = 'What rule do you wish to know, my master?'
    elif subject == 'list':
        list_of_files = os.listdir('rules')
        pattern = '*.txt'
        list_of_rules = [entry.replace('.txt', '') for entry in list_of_files if fnmatch.fnmatch(entry, pattern)]
        response = 'The following rules can be entered in the command:\n\n'
        for rule in list_of_rules:
            response = response + rule + '\n'
    else:
        try:
            response = read_rule(subject, *especification)
        except FileNotFoundError:
            response = 'No such rule'
    await ctx.send(response)


bot.run(TOKEN)
