import aiohttp
import discord
from yarl import URL

async def weather(ctx, cmd, token):
    cmd = ','.join(cmd)

    # Perform the request
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q={cmd}&units=imperial&appid={token}') as response:
            if response.status == 200:
                try:
                    resp_json = await response.json()

                    # Get relevant fields
                    title = resp_json['name'] + ', ' + resp_json['sys']['country']
                    description = resp_json['weather'][0]['description'].capitalize() + '.'
                    thumbnail = resp_json['weather'][0]['icon']
                    temp = resp_json['main']['temp']
                    humidity = resp_json['main']['humidity']
                    pressure = resp_json['main']['pressure']

                    # Produce embed
                    embed = await getWeatherEmbed(title, description, thumbnail, temp, humidity, pressure)

                    # Send msg
                    await ctx.send(embed=embed)
                except Exception as e:
                    print(e)
                    await ctx.send('I didn\'t recognize that command. Try asking me: **!help weather**')
            else:
                await ctx.send('I didn\'t recognize that command. Try asking me: **!help weather**')

# Returns an embed for the weather
async def getWeatherEmbed(title, description, thumbnail, temp, humidity, pressure):
    embed = discord.Embed(title=title, description=description)
    embed.set_thumbnail(url=f'http://openweathermap.org/img/w/{thumbnail}.png')
    embed.add_field(name='Temp', value=f'{temp} °F', inline=True)
    embed.add_field(name='Humidity', value=f'{humidity}%', inline=True)
    embed.add_field(name='Pressure', value=f'{pressure} hPa', inline=True)
    embed.set_footer(text='Provided by OpenWeather')
    return embed