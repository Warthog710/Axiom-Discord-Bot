import json
from discord.ext import commands
from dice import parseDice
from randomFact import randomFact

#Invite URL: https://discord.com/oauth2/authorize?client_id=774061395301761075&scope=bot&permissions=8

#TODO: In dice rolling... have it @ the user who asked it to roll
#TODO: Move bot token out of code... Into local config file?
#TODO: Name generation? Weather? Time-zone conversion?
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
#TODO: React in some manner when 69 is said...
#TODO: Handle if a server joins when the bot is down... No prefix is set
#TODO: Rework how dice.py parses the string... it doesn't support negatives and stuff

#Load config
with open('./Config/config.json', 'r') as configFile:
    configData = configFile.read()
    config = json.loads(configData)

#Used to get the prefix for the server
def getPrefix(client, message):
    with open('./Config/prefixes.json', "r") as file:
        prefixes = json.load(file)

    return  prefixes[str(message.guild.id)]

#Bot command prefix
bot = commands.Bot(command_prefix=getPrefix)

#Bot starts with "!" as the default prefix
#Function runs when a server joins and sets a default prefix
@bot.event
async def on_guild_join(guild):
    with open ('./Config/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '!'

    with open ('./Config/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

    print("joined")

#Removes the server prefix recorded if the bot is removed from the server
@bot.event
async def on_guild_remove(guild):
    with open ('./Config/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open ('./Config/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

#This can be called to change the prefix of the bot on a server
#? Only a member with manage guild permissions can do this
@bot.command(name='changePrefix', help='Change the prefix the bot uses on this server\nUsage !changePrefix <desired_prefix>')
@commands.has_permissions(manage_guild=True)
async def changePrefix(ctx, prefix):
    with open('./Config/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(ctx.guild.id)] = prefix

    with open('./Config/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

    await ctx.send('Prefix successfully changed to {}'.format(prefix))

#On ready event... print the bot is ready
@bot.event
async def on_ready():
    print('Bot is ready...')

#Defines the !roll command
#? Note *cmd means everything after !roll is sent as a tuple
@bot.command(name='roll', help='Roll a dice!\nUsage: !roll <number_of_dice> d <number_of_sides> +/- <modifier>')
async def rollDice(ctx, *cmd):
    await(parseDice(ctx, cmd))

#Polls a third party API for a random fact
@bot.command(name='random', help='Get a random fact!\nUsage: !random or !random daily')
async def getRandomFact(ctx, *cmd):
    await(randomFact(ctx, cmd, config))

#Simple message event
#@bot.event
#async def on_message(message):
    #Don't do anything if the bot sent the message
#    if message.author == bot.user:
#        return

#    await message.channel.send("Hi, my name is Axiom!")


#Runs the bot with the access code...
bot.run(config['discordToken'])