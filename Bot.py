from MarkovNameGenerator import markovNameGenerator
import json
import asyncio

from discord.ext import commands
from datetime import datetime
from Dice import parseDice
from RandomFact import randomFact
from Scheduler import scheduler
from MarkovNameGenerator import markovNameGenerator
from Weather import weather

# Invite URL: https://discord.com/oauth2/authorize?client_id=774061395301761075&scope=bot&permissions=8

# TODO: Weather? Time-zone conversion?
# TODO: Moderation using Google's API?
# TODO: Coinflip?
# TODO: Automatically assign roles?
# TODO: Greet a user that joins the server?
# TODO: Keep highest/lowest dice... and bounded dice?
# TODO: Reminders to a specific user?
# TODO: Scheduler... schedule an event that @'s a certain role(s) at the given event time (add, show, edit, delete events)
# TODO: Bot says "nice" everytime 69 is in a message
# TODO: Add !creator message to give sage wisdom on who programmed the bot
# TODO: Fact checking using Google's API
# TODO: Some form of Cogs support...
# TODO: React in some manner when 69 is said...

# Load config
with open('./Config/config.json', 'r') as config:
    config = json.loads(config.read())

# Load prefixes
with open('./Config/prefixes.json', 'r') as prefixes:
    prefixes = json.load(prefixes)

# Used to get the prefix for the server
def getPrefix(client, message):
    if str(message.guild.id) in prefixes:
        return prefixes[str(message.guild.id)]
    else:
        prefixes[str(message.guild.id)] = '!'

        # Dump the new prefix into the JSON
        with open('./Config/prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)

        # Return the default prefix
        return '!'

# Set Bot command prefix
bot = commands.Bot(command_prefix=getPrefix)
sched = scheduler()
nameGen = markovNameGenerator(2)

async def scheduling_task():
    await bot.wait_until_ready()

    while not bot.is_closed():
        await sched.performTasks(bot)
        #channel = bot.get_channel(id=774063966258987048)
        #await channel.send(f'Count: {count}')

        # Wait until the next minute
        await asyncio.sleep(60 - datetime.now().second)

@bot.event
async def on_guild_join(guild):
    prefixes[str(guild.id)] = '!'

    with open('./Config/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

    print(f'Joined: {guild}')

@bot.event
async def on_guild_remove(guild):
    prefixes.pop(str(guild.id))

    with open('./Config/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

# This can be called to change the prefix of the bot on a server
# ? Only a member with manage guild permissions can do this
@bot.command(name='changePrefix', help='Change the prefix the bot uses on this server\n\nUsage !changePrefix <desired_prefix>')
@commands.has_permissions(manage_guild=True)
async def changePrefix(ctx, prefix):
    # Only accept prefixes of a single char
    if len(prefixes) == 1:
        prefixes[str(ctx.guild.id)] = prefix

        with open('./Config/prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)

        await ctx.send(f'Prefix successfully changed to: **{prefix}**')
    else:
        await ctx.send('Prefix must be a single character.')

@bot.event
async def on_ready():
    print('Axiom Discord Bot Successfully Started!')

# Defines the !roll command
# ? Note *cmd means everything after !roll is sent as a tuple
@bot.command(name='roll', help='Roll a dice! Modifier is optional.\nUsage: !roll <number_of_dice>d<number_of_sides> +/- <modifier>')
async def rollDice(ctx, *cmd):
    await(parseDice(ctx, cmd))

# Polls a third party API for a random fact
@bot.command(name='random', help='Get a random fact!\nUsage: !random or !random daily')
async def getRandomFact(ctx, *cmd):
    await(randomFact(ctx, cmd, config))

# Reminder
# ? In form: !reminder <month>/<day>/<year> <hour>:<minutes>PM/AM <Alert_Level> <Message>
@bot.command(name='reminder', aliases=['r'], help='Set a reminder. This reminder will be sent in the same channel it was requested from.\n\nUsage: !reminder <month>/<day>/<year> <hour>:<minutes>PM/AM <alert_level> <message>\n\nAlert level can either be personal (@author), here (@here), or everyone (@everyone).')
async def reminder(ctx, date, time, alert_level, *message):
    try:
        message = ' '.join(message)
        task_id = await sched.addTask(ctx.message.author.id, 'REMINDER', alert_level.upper().strip(), date, time, ctx.channel.id, ctx.message.id, message, bot)
    except Exception as e:
        print(e)
        await ctx.send('I didn\'t recognize that command. Try asking me: **!help reminder**')
        return

    # React with a +1 and send a confirmation message to the message author
    await ctx.message.add_reaction('👍')
    await ctx.author.send(f'Reminder saved! If you wish to delete this reminder please use the command ``!deleteReminder {task_id}`` (prefix varies): ```{message}```')

# Personal reminder
# ? in form: !personalReminder <month>/<day>/<year> <hour>:<minutes>PM/AM <Message>
@bot.command(name='personalReminder', aliases=['pr'], help='Set a personal reminder. This reminder will be sent as a PM to the author.\n\nUsage: !personalReminder <month>/<day>/<year> <hour>:<minutes>PM/AM <message>')
async def personalReminder(ctx, date, time, *message):
    try:
        message = ' '.join(message)
        task_id = await sched.addTask(ctx.message.author.id, 'PM', 'PERSONAL', date, time, ctx.channel.id, ctx.message.id, message, bot)
    except Exception as e:
        print(e)
        await ctx.send('I didn\'t recognize that command. Try asking me: **!help personalReminder**')
        return

    # React with a +1 and send a confirmation message to the message author
    await ctx.message.add_reaction('👍')
    await ctx.author.send(f'Personal reminder saved! If you wish to delete this reminder please use the command ``!deleteReminder {task_id}`` (prefix varies): ```{message}```')

# Self-Destruct, deletes the message at a specific time and date
# ? In form: !selfDestruct <month>/<day>/<year> <hour>:<minutes>PM/AM
@bot.command(name='selfDestruct', aliases=['sd'], help='Deletes the message at a given time and date.\n\nUsage: !selfDestruct <month>/<day>/<year> <hour>:<minutes>PM/AM')
async def selfDestruct(ctx, date, time, *message):
    try:
        message = ' '.join(message)
        task_id = await sched.addTask(ctx.message.author.id, 'SELF-DESTRUCT', 'PERSONAL', date, time, ctx.channel.id, ctx.message.id, message, bot)
    except Exception as e:
        print(e)
        await ctx.send('I didn\'t recognize that command. Try asking me: **!help selfDestruct**')
        return

    # React with a bomb and send a confirmation message to the message author
    await ctx.message.add_reaction('💣')
    await ctx.author.send(f'Self-Destruct task saved! If you wish to delete this task please use the command ``!deleteTask {task_id}`` (prefix varies): ```{message}```')

@bot.command(name='deleteReminder', aliases=['dr', 'deleteTask', 'dt'], help='Deletes a reminder or task.\n\nUsage: !deleteReminder <id>\n\nWhen a reminder/task is set, the Id of that reminder will be PM\'d to the author.')
async def deleteReminder(ctx, task_id):
    await sched.delTask(ctx, task_id)

@bot.command(name='name', help='Generates a random name.\n\nUsage: !name <length>\n\nThe length parameter is optional. If it is not set, the name generated will be 3-10 characters in length. Note, due to the algorithm used for generation, it is possible that a returned name is less than the requested amount of characters.')
async def generateName(ctx, length=None):
    try:
        if length != None:
            length = int(length)
            if length > 30 or length < 3:
                await ctx.send(f'Names can only be generated with length 3-30.')
                return

        name = await nameGen.generateName(length)
        await ctx.send(f'{ctx.message.author.mention} {name}')
    except Exception as e:
        print(e)
        await ctx.send('I didn\'t recognize that command. Try asking me: **!help name**')

@bot.command(name='weather', help='Get the current weather.\n\nUsage: !weather <city> <state> <country>\n\nBoth the state and country parameters are optional. However, if an error occurs or the wrong city is returned try specifiyng them. In addition, please ensure parameters are seperated by a single space.')
async def getWeather(ctx, *cmd):
    await weather(ctx, cmd, config['openWeatherToken'])

#Setup the scheduling task
bot.loop.create_task(scheduling_task())

# Runs the bot with the access code...
bot.run(config['discordToken'])
