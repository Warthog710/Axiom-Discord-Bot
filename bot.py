import discord
from discord.ext import commands
from dice import parseDice

#Bot token
token = 'Nzc0MDYxMzk1MzAxNzYxMDc1.X6SS2g.EMQnjOhDuW-_5Mj3lRHgVnFm0dE'

#TODO: In dice rolling... have it @ the user who asked it to roll
#TODO: Move bot token out of code... Into local config file?

#Bot command prefix
bot = commands.Bot(command_prefix='!')

#On ready event... print the bot is ready
@bot.event
async def on_ready():
    print('Bot is ready...')

#Defines the !roll command
#? Note *cmd means everything after !roll is sent as a tuple
@bot.command(name='roll', help='Roll a dice!\nUsage: !roll <number_of_dice>D<number_of_sides> +/- <modifier>')
async def rollDice(ctx, *cmd):
    await(parseDice(ctx, cmd))

#Simple message event
#@bot.event
#async def on_message(message):
    #Don't do anything if the bot sent the message
#    if message.author == bot.user:
#        return

#    await message.channel.send("Hi, my name is Axiom!")


#Runs the bot with the access code...
bot.run(token)