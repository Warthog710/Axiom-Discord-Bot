import random
import re

# Command in form: !roll 4d20 +4 or !roll 3d6 - 3, or !roll 4d8
async def parseDice(ctx, cmd):
    try:
        cmd = list(cmd)

        # If the length of commands is > 1, we have a modifier
        if len(cmd) > 1:
            dice_num, dice_sides = re.split('d|D', cmd[0])
            dice_num = int(dice_num)
            dice_sides = int(dice_sides)
            del(cmd[0])
            mod = int(''.join(cmd))
        else:
            dice_num, dice_sides = re.split('d|D', cmd[0])
            dice_num = int(dice_num)
            dice_sides = int(dice_sides)
            mod = 0

        #If the user asked to roll less than 1 dice
        if dice_num < 1:
            await ctx.send(f'It\'s physically impossible to roll {dice_num} dice... :face_with_monocle:')
            return

        #If the user asked to roll a dice with less than 1 side
        #? Supports dice with >=1 side.
        if dice_sides < 1:
            await ctx.send(f'I\'ll roll a dice with {dice_sides} sides once you tell me how they work... :thinking:')
            return

        #If the user asked to roll greater than 1000 dice
        if dice_num > 1000:
            await ctx.send('I currently can\'t roll more than 1000 dice :sob:')
            return

        #If the user wants to roll 1 dice
        if dice_num == 1:
            msg = f' rolling {dice_num}d{dice_sides}'

            #Only show mod if its not zero
            if mod != 0:
                msg += f' with modifier {mod}:\n'
            else:
                msg += ':\n'

            msg += f':game_die: **{random.randint(1, dice_sides) + mod}** :game_die:'

            #Send the msg
            await ctx.send(ctx.message.author.mention + msg)
        
        elif dice_num <= 10:
            msg = f'{ctx.message.author.mention} rolling {dice_num}d{dice_sides}'

            #Only show mod if its not zero
            if mod != 0:
                msg += f' with modifier {mod}:\n```Dice\tRoll\tMod\n----\t----\t---\n'

                #Do the roll!
                total = 0
                for _ in range(dice_num):
                    rand = random.randint(1, dice_sides) + mod
                    total += rand
                    msg += '{:^4}\t'.format(('d' + str(dice_sides))) + '{:^4}\t'.format(str(rand)) + '{:^3}\n'.format(str(mod))

                msg += f'\nAverage Roll: {round(total/dice_num, 2)}\nTotal: {total}```'
                await ctx.send(msg)
            else:
                msg += ':\n```Dice\tRoll\n----\t----\n'

                #Do the roll!
                total = 0
                for _ in range(dice_num):
                    rand = random.randint(1, dice_sides)
                    total += rand
                    msg += '{:^4}\t'.format(('d' + str(dice_sides))) + '{:^4}\n'.format(str(rand))

                msg += f'\nAverage Roll: {round(total/dice_num, 2)}\nTotal: {total}```'
                await ctx.send(msg)

        #We have greater than 10 dice, just show the total
        else:
            msg = f' rolling {dice_num}d{dice_sides}'

            #Only show mod if its not zero
            if mod != 0:
                msg += f' with modifier {mod}:\n'
            else:
                msg += ':\n'

            #Do the roll!
            total = 0
            for _ in range(dice_num):
                total += random.randint(1, dice_sides) + mod

            msg += f':game_die: **{total}** :game_die:'

            #Send the msg
            await ctx.send(ctx.message.author.mention + msg)

    # If any exception occurs
    except Exception as e:
        await ctx.send("I didn't recognize that command. Try asking me: **!help roll**")
