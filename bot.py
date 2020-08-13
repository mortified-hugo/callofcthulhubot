import os

import fnmatch
import discord

import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv

import numpy as np
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='%')


def read_rule(*rule):
    expression = ''
    for word in rule:
        expression = expression + '/' + word
        print(expression)
    with open(f'rules{expression}.txt', mode='r') as file:
        answer = file.read()
    return answer


def check_date(log_date):
    if int(log_date[0]) <= 0 or int(log_date[0]) > 12:
        return True
    elif int(log_date[1]) <= 0 or int(log_date[1]) > 31:
        return True
    elif int(log_date[0]) in [2, 4, 6, 9, 11] and int(log_date[1]) == 31:
        return True
    elif int(log_date[0]) == 2 and int(log_date[1]) == 30:
        return True
    else:
        return False


def check_end_month(log_date):
    if int(log_date[0]) in [1, 3, 7, 8, 10, 12]:
        if int(log_date[1]) == 31:
            return True
        else:
            return False
    elif int(log_date[0]) in [4, 6, 9, 11]:
        if int(log_date[1]) == 30:
            return True
        else:
            return False
    elif int(log_date[0]) == 2:
        if int(log_date[2]) % 4 and int(log_date[2]) != 1900:
            if log_date[1] == 29:
                return True
            else:
                return False
        else:
            if log_date[1] == 28:
                return True
            else:
                return False


def list_file(file_type, list_of_files):
    pattern = f'*{file_type}'
    end_list = [entry.replace(file_type, '') for entry in list_of_files if fnmatch.fnmatch(entry, pattern)]
    return end_list


# Connection

@bot.event 
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='rule', help='Quick guide for the game rules')  # Rule Library
async def get_rule(ctx, subject='', *especification):
    if subject == '':
        response = 'What rule do you wish to know, my master?'
    elif subject == 'list':
        rules_list = os.listdir('rules')
        list_of_rules = list_file('.txt', rules_list)
        response = '```The following rules can be entered in the command:\n\n'
        for rule in list_of_rules:
            response = response + rule + '\n'
        response = response + '```'
    elif subject in ['link', 'serbia']:
        response = read_rule(subject, *especification)
    else:
        try:
            response = "```" + read_rule(subject, *especification) + "```"
        except FileNotFoundError:
            response = 'No such rule'
    await ctx.send(response)


@bot.command(name='dhole', help="Dhole's House website for making characters")  # Dhole Reference
async def dhole_url(ctx):
    response = 'https://www.dholeshouse.org/Default'
    await ctx.send(response)


@bot.command(name='date', help="Pulls info from the date from wikipedia(MM/DD/YYYY)")  # Get's data from wikipedia
async def get_date(ctx, date):
    rex = re.compile("^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$")
    if not rex.match(date):
        response = 'Wrong Format for the date, please enter MM/DD/YYYY'
    else:
        log = date.split('/')
        months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
                  '05': 'May', '06': 'June', '07': 'July', '08': 'August',
                  '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
        if check_date(log):
            response = 'Wrong date, be sure to use the MM/DD/YYYY format'
        else:
            log[1] = (str(int(log[1])))
            next_day = str(int(log[1]) + 1)
            url = f"https://en.wikipedia.org/wiki/{months[log[0]]}_{log[2]}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, features='html.parser')
            if check_end_month(log):
                end_point = 'References'
            else:
                end_point = f"{months[log[0]]} {next_day}, {log[2]} ("
            info = soup.text[soup.text.rfind(f"{months[log[0]]} {log[1]}, {log[2]} (")
                             : soup.text.rfind(end_point)]
            response = re.sub("[\[].*?[\]]", "", info)
            if response == '':
                response = "Something odd happened, maybe wikipedia does't have info on that month or that day"
            elif len(response) > 2000:
                response = response[:1990] + '...'
    await ctx.send(response)


@bot.command(name='show', help='Shows image of character in library')
async def get_image(ctx, image_name):
    if image_name == '':
        response = "Please add image name to %show command"
    elif image_name == 'list':
        images_list = os.listdir('images')
        list_of_images = list_file('.jpg', images_list) + list_file('.png', images_list)
        response = '```The following rules can be entered in the command:\n\n'
        for image in list_of_images:
            response = response + image + '\n'
        response = response + '```'
    else:
        try:
            with open(f'images/{image_name}.jpg', 'rb') as image:
                response = discord.File(image)
        except FileNotFoundError:
            try:
                with open(f'images/{image_name}.png', 'rb') as image:
                    response = discord.File(image)
            except FileNotFoundError:
                response = "``` image not found ```"
    if isinstance(response, type('str')):
        await ctx.send(response)
    else:
        await ctx.send(file=response)


bot.run(TOKEN)
