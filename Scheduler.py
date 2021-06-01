import heapq
import uuid

from discord.ext import *
from datetime import datetime

#! Reminder Types:
#   Personal Reminder - PM's the author the message at the given time
#   Reminder - Sends a message in the same channel using the author as the @ msg
#   Self-Destruct - Deletes a message at the given time

#! Alert Levels:
#   HERE - @here
#   EVERYONE - @everyone
#   PERSONAL - @author


class scheduler:
    def __init__(self):
        self.__task_list = self.__readTasksFromDisk()

    # ? Reads the top of the heap and performs the task if it is ready.
    async def performTasks(self, bot):
        now = datetime.now()

        # Perform tasks if they are ready
        while True:
            # If no tasks exist break
            if len(self.__task_list) <= 0:
                break

            # Else if the next task is not ready, break
            if now <= datetime.strptime(self.__task_list[0].scheduled_time, '%m/%d/%Y %H:%M'):
                break

            # Else, do the task
            else:
                current_task = heapq.heappop(self.__task_list)
                #print(f'Doing a task: {current_task}')

                # Perform a standard reminder task
                if 'REMINDER' in current_task.task_type:
                    if 'EVERYONE' in current_task.alert_level:
                        await bot.get_channel(id=current_task.channel_id).send(f'@everyone {current_task.message}')                        
                    elif 'HERE' in current_task.alert_level:
                        await bot.get_channel(id=current_task.channel_id).send(f'@here {current_task.message}')                        
                    else:
                        await bot.get_channel(id=current_task.channel_id).send(f'<@{current_task.author}> {current_task.message}')

                # Perform a PM reminder
                elif 'PM' in current_task.task_type:
                    try:
                        author = await bot.fetch_user(current_task.author)
                        await author.send(current_task.message)
                    except Exception as e:
                        print(e)
                        print('Failed to send a personal reminder...')

                # Else, it must be a self-destruct task
                else:
                    try:
                        message = await bot.get_channel(id=current_task.channel_id).fetch_message(current_task.message_id)
                        author = await bot.fetch_user(current_task.author)
                        await message.delete()
                        await author.send(f'The requested message was successfully deleted: ```{current_task.message}```')
                    except Exception as e:
                        print(e)
                        print('Failed to delete a message')

                # Dump tasks to disk to save them
                self.__dumpTasksToDisk()

    # ? Parses the passed discord message and adds it to the task heap
    async def addTask(self, author, task_type, alert_level, date, time, channel_id, message_id, message, bot):
        print(f'Got:\nAuthor: {author}\nTask Type: {task_type}\nAlert Lvl: {alert_level}\nDate: {date}\nTime: {time}\nChannel Id: {channel_id}\nMsg: {message}')

        # Make sure the date is valid
        task_date_time = self.__parseDateAndTime(date, time)
        now = datetime.now()

        if now >= task_date_time:
            await bot.get_channel(id=int(channel_id)).send('The date and/or time was invalid. Try asking me: **!help reminder**')
            return
        else:
            task_date_time = task_date_time.strftime('%m/%d/%Y %H:%M')

        # Verify alert level is valid
        if not 'HERE' in alert_level and not 'EVERYONE' in alert_level and not 'PERSONAL' in alert_level:
            await bot.get_channel(id=int(channel_id)).send('The alert level was invalid. Try asking me: **!help reminder**')
            return

        # Verify task_type is valid
        if not 'REMINDER' in task_type and not 'SELF-DESTRUCT' in task_type and not 'PM' in task_type:
            await bot.get_channel(id=int(channel_id)).send('The task type was invalid. Try asking me: **!help reminder**')
            return

        # Add the task
        print('Adding task...')
        new_task = task(None, author, task_type, alert_level, task_date_time, channel_id, message_id, message)
        heapq.heappush(self.__task_list, new_task)
        self.__dumpTasksToDisk()

        # Return the task id
        return new_task.id

    # ? Parses the passed discord message and delete the message from the heap if it exists
    async def delTask(self, ctx, task_id):
        for task in self.__task_list:
            if task.id == task_id:
                if task.author == ctx.author.id:
                    self.__task_list.remove(task)
                    heapq.heapify(self.__task_list)
                    self.__dumpTasksToDisk()

                    # Inform user of successful deletion
                    await ctx.message.add_reaction('👍')
                    await ctx.author.send(f'Task {task_id} successfully deleted.')
                    return

        await ctx.send('I could not find that task. Please use the task Id that was sent. Also note, you must be the author of the task to delete it.')

    # ? Called to write tasks to disk in a file. This saves tasks in case the bot halts
    def __dumpTasksToDisk(self):
        task_file = open('./Config/scheduler_tasks.txt', 'w')

        for task in self.__task_list:
            task_file.write(task.writeToDisk())

        task_file.close()

    # ? Called when the bot starts up to maintain tasks
    def __readTasksFromDisk(self):
        task_file = open('./Config/scheduler_tasks.txt', 'r')
        task_list = []

        # Expects 8 lines per task
        task_lines = task_file.readlines()
        for x in range(0, len(task_lines), 8):
            new_task = task(task_lines[x].strip(), task_lines[x + 1].strip(
            ), task_lines[x + 2].strip(), task_lines[x + 3].strip(), task_lines[x + 4].strip(), 
            task_lines[x + 5].strip(), task_lines[x + 6].strip(), task_lines[x + 7])

            task_list.append(new_task)

        task_file.close()

        # Return as a heap
        heapq.heapify(task_list)
        return task_list

    def __parseDateAndTime(self, date, time):
        #Convert time to 24hr
        if 'PM' in time.upper():
            hour, minutes = time.split(':')
            minutes = minutes.upper().replace('PM', '')
            hour = str(int(hour) + 12)
            time = hour + ':' + minutes
        else:
            time = time.upper().replace('AM', '')

        #Verify the date is correct
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


# ? Task container
class task(object):
    def __init__(self, id, author, task_type, alert_level, scheduled_time, channel_id, message_id, message):
        if id == None:
            self.id = str(uuid.uuid4())
        else:
            self.id = str(id)

        self.author = int(author)
        self.task_type = str(task_type)
        self.alert_level = str(alert_level)
        self.scheduled_time = str(scheduled_time)
        self.channel_id = int(channel_id)
        self.message_id = int(message_id)
        self.message = str(message)

    # ? Returns a string containing the task data
    def writeToDisk(self):
        return f'{self.id}\n{self.author}\n{self.task_type}\n{self.alert_level}\n{self.scheduled_time}\n{self.channel_id}\n{self.message_id}\n{self.message}\n'

    # ? < operator override
    def __lt__(self, other):
        return datetime.strptime(self.scheduled_time, '%m/%d/%Y %H:%M') < datetime.strptime(other.scheduled_time, '%m/%d/%Y %H:%M')

    # ? Used when a printing the heap
    def __repr__(self):
        return f'\nId: {self.id}\nAuthor: {self.author}\nTask Type: {self.task_type}\nAlert Level: {self.alert_level}\nScheduled Time: {self.scheduled_time}\nChannel ID: {self.channel_id}\nMessage ID: {self.message_id}\nMessage: {self.message}\n'
