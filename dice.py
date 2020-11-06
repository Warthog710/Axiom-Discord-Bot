import random
import re

from discord.ext.commands.core import command

#Maps number of dice rolled to the word
diceMap = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

async def parseDice(ctx, cmd):
    try:
        total = 0
        modifier = '+'
        cmdString = ''.join(cmd)

        #Set modifier if negative
        if '-' in cmdString:
            modifier = ''

        cmdString = cmdString.lower()
        commands = re.split('d|\+|-', cmdString)

        #Convert list of strings to ints
        commands = [int(i) for i in commands]

        #Make sure the user didn't ask to role zero dice
        if (commands[0] == 0):
            await ctx.send("Its physically impossible to roll 0 dice... :face_with_monocle:")
            return

        #Add a zero modifier if no modifier was passed
        if (len(commands) == 2):
            commands.append(0)  

        #If the modifier was negative... negate the modifier
        if (modifier == ''):
            commands[2] = commands[2] * -1

        #if the user only wants to rule 1 dice... just do it
        if (commands[0] == 1):
            await ctx.send("Rolling " + diceMap[commands[0] - 1] + " d" + str(commands[1]) + " with " + modifier + str(commands[2]) + " modifier...\n")   
            await ctx.send(":game_die: " + str((random.randint(1, commands[1]) + commands[2])) + " :game_die:")

        elif (commands[0] > 1000):
            await ctx.send("I can't currently roll more than 1000 dice :sob:")

        #If the user wants to roll more than 10 dice... just do it
        elif (commands[0] > 10):
            await ctx.send("Rolling " + diceMap[commands[0] - 1] + " d" + str(commands[1]) + " with " + modifier + str(commands[2]) + " modifier...\n")    
            for x in range(commands[0]):
                total += random.randint(1, commands[1]) + commands[2]
            await ctx.send(":game_die: " + str(total) + " :game_die:")

        else:
            await ctx.send("Rolling " + diceMap[commands[0] - 1] + " d" + str(commands[1]) + " with " + modifier + str(commands[2]) + " modifier...\n")   
            msg = '```Dice\tRoll\tMod\n----\t----\t---\n'
            for x in range(commands[0]):
                rand = random.randint(1, commands[1]) + commands[2]
                total += rand
                msg += '{:4}'.format(('d' + str(commands[1]))) + '\t' + '{:4}'.format(str(rand)) + '\t' + '{:3}'.format(modifier + str(commands[2])) + '\n'

            msg += '\nAverage Roll: ' + str(round(total/commands[0], 2)) + '\n' + 'Total: ' + str(total) + '```'
            await ctx.send(msg)

    #If any exception occurs
    except Exception:
        await ctx.send("I didn't recognize that command. Try asking me: **!help roll**")    