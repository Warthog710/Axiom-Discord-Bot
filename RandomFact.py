import aiohttp

async def randomFact(ctx, cmd, config):
    cmdString = ''.join(cmd)
    cmdString = cmdString.lower()  

    #User requested the random fact of the day
    if "daily" in cmdString:
        async with aiohttp.ClientSession() as session:
            async with session.get(config['randomDailyFact']) as response:
                if response.status == 200:
                    responseText = await response.json()
                    await ctx.send(ctx.message.author.mention + " " + str(responseText['text']))
                else:
                    await ctx.send('Failed to get a response. Somebody must be calculating Pi on the server :confounded:')

    #Else the user requested just a random fact
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(config['randomFact']) as response:
                if response.status == 200:
                    responseText = await response.json()
                    await ctx.send(ctx.message.author.mention + " " + str(responseText['text']))
                else:
                    await ctx.send('Failed to get a response. Somebody must be calculating Pi on the server :confounded:')
