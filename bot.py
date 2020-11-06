import discord
import json
from discord.ext import commands
from dice import parseDice

#Load config
with open('config.json', 'r') as configFile:
    configData = configFile.read()
    config = json.loads(configData)

#TODO: In dice rolling... have it @ the user who asked it to roll
#TODO: Move bot token out of code... Into local config file?
#TODO: Random facts? Name generation? Weather? Time-zone conversion?
#TODO: Moderation using Google's API?
#TODO: Coinflip?
#TODO: Automatically assign roles?
#TODO: Greet a user that joins the server?
#TODO: Keep highest/lowest dice... and bounded dice?
#TODO: Reminders to a specific user?
#TODO: Scheduler... schedule an event that @'s a certain role(s) at the given event time (add, show, edit, delete events)
#TODO: Bot says "nice" everytime 69 is in a message
#TODO: Add !creator message to give sage wisdom on who programmed the bot
#TODO: Fact checking using Google's API
#TODO: Some form of Cogs support...

#Bot command prefix
bot = commands.Bot(command_prefix='!')

#On ready event... print the bot is ready
@bot.event
async def on_ready():
    print('Bot is ready...')

#Defines the !roll command
#? Note *cmd means everything after !roll is sent as a tuple
@bot.command(name='roll', help='Roll a dice!\nUsage: !roll <number_of_dice> d <number_of_sides> +/- <modifier>')
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
bot.run(config['discordToken'])