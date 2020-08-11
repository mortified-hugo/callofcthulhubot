import os
import discord
from dotenv import load_dotenv
import numpy as np

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


# Functions


def answer_gods(god):
    with open(f'gods/{god}.txt', mode='r') as file:
        possible_answers = file.readlines()
        answer = possible_answers[np.random.randint(0, len(possible_answers) - 1)]
    return answer


def evaluate_triggers(trigger, evaluator):
    return any([True for word in trigger if word in evaluator])


# Events


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    shub_niggurath_triggers = ['Castor', 'Shub-Niggurath', 'the Black Goat', 'The Black Goat', 'black goat']
    yog_sothoth_triggers = ['Yog-Sothoth', 'he who knows all', 'he who sees all']
    nyarlathotep_triggers = ["The Bringer of Caos", 'the Faceless God', 'The Coptic Magician']
    necronomicon_triggers = ['necronomicon', 'Necronomicon']
    azathoth_triggers = ['Azathoth']
    my_creator = "The Ancient Elder Things who ruled the Earth"

    if evaluate_triggers(shub_niggurath_triggers, message.content):
        response = answer_gods('shub')
    elif evaluate_triggers(yog_sothoth_triggers, message.content):
        response = answer_gods('yog')
    elif evaluate_triggers(nyarlathotep_triggers, message.content):
        response = answer_gods('nyarla')
    elif evaluate_triggers(necronomicon_triggers, message.content):
        response = answer_gods('necronomicon')
    elif message.content == "Who created you?":
        response = my_creator
    elif 'John Smith' in message.content:
        response = answer_gods('john_smith')
    elif evaluate_triggers(azathoth_triggers, message.content):
        response = answer_gods('azathoth')
    else:
        response = None

    if response is not None and np.random.rand() > 0.8 or response == my_creator:
        await message.channel.send(response)


client.run(TOKEN)
