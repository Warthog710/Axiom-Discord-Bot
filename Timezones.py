import pytz
from datetime import datetime

class timezone:
    def __init__(self):
        self.__zones_dict = {}

        # Create reference dictionary
        for item in pytz.common_timezones:
            temp = item.split('/')[0]

            if temp.upper() in self.__zones_dict:
                self.__zones_dict[temp.upper()].append(item)
            else:
                self.__zones_dict[temp.upper()] = [item]

    # Performed the timezone: passed_timezone -> desired_timezone
    async def calculate_timezone(self, ctx, date, time, current_timezone, desired_timezone):
        # Convert date_time to desired time zone
        date_time = self.__parseDateAndTime(date, time)

        try:
            source_tz = pytz.timezone(current_timezone)
            dst_tz = pytz.timezone(desired_timezone)
        except pytz.UnknownTimeZoneError:
            await ctx.send('I failed to recognize one or both of the timezones specified. Try using **!acceptableTimezones <zone>** to see a list of allowed timezones')
            return

        date_time_with_zone = source_tz.localize(date_time)        
        dst_time_with_zone = date_time_with_zone.astimezone(dst_tz)
        dst_time_str = datetime.strftime(dst_time_with_zone, '%I:%M%p %m/%d/%Y')
        src_time_str = datetime.strftime(date_time, '%I:%M%p %m/%d/%Y')

        await ctx.send(ctx.author.mention + f' {current_timezone} {src_time_str} -> {desired_timezone} {dst_time_str}')        

    # Sends a formatted list of available timezones to the user if requested
    async def send_timezone_list(self, ctx, zone):
        if zone.upper() in self.__zones_dict:
            msg = f'List of acceptable timezones for {zone}:\n```'
            msg += '\n'.join(self.__zones_dict[zone.upper()])
            msg += '```'

            # Discord only accepts messages with up to 2k characters
            if len(msg) > 2000:
                # ! Bad fix: don't split on a timezone
                temp_list = msg.split('\n')

                # ? It is very unlikely that a timezone list is greater than 4k characters
                msg1, msg2 = self.__split_list(temp_list, 2)
                msg1 = '\n'.join(msg1) + '```'
                msg2 = '\n'.join(msg2)
                msg2 = '```' + msg2

                await ctx.author.send(msg1)
                await ctx.author.send(msg2)
            
            # Message is already below size limit
            else:
                await ctx.author.send(msg)             

        # Invalid key      
        else:
            await ctx.send('I didn\'t recognize that command. Try asking me: **!help acceptableTimezones**')


    def __split_list(self, sList, wanted_parts=1):
        length = len(sList)
        return [sList[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]

    def __parseDateAndTime(self, date, time):
        # Convert time to 24hr
        if 'PM' in time.upper():
            hour, minutes = time.split(':')
            minutes = minutes.upper().replace('PM', '')
            hour = str(int(hour) + 12)
            time = hour + ':' + minutes
        else:
            time = time.upper().replace('AM', '')

        # Verify the date is correct
        date = date.split('/')
        month = date[0]
        day = date[1]

        if len(month) < 2:
            month = '0' + month
        
        if len(day) < 2:
            day = '0' + day

        if len(date) >= 3:
            current_year = str(datetime.now().year)
            year = date[2]
            if len(year) < 4:
                year = current_year[0] + current_year[1] + year
        else:
            year = datetime.now().year

        date = f'{month}/{day}/{year} {time}'
        return datetime.strptime(date, '%m/%d/%Y %H:%M')
        