import heapq
import datetime

class scheduler:
    def __init__(self, bot):
        self.__bot = bot

        e1 = task('test', 'test', 3, 'test', 'test')
        e2 = task('test', 'test', 2, 'test', 'test')
        e3 = task('test', 'test', 2, 'test', 'test')
        task_list = [e1, e2, e3]

        print(datetime.datetime.now())

        heapq.heapify(task_list)

        print(task_list)
        
        print(5)

    async def printTask(self):
        #channel = self.__bot.get_channel(id=774063966258987048)
        #await channel.send(f'Count: {1}')
        #print(2)
        pass

#Holds a task to be performed by the scheduler
class task(object):
    def __init__(self, author, task_type, scheduled_time, channel_id, message):
        self.author = author
        self.task_type = task_type
        self.scheduled_time = scheduled_time
        self.channel_id = channel_id
        self.message = message

    # < operator override
    def __lt__(self, other):
        return self.scheduled_time < other.scheduled_time

    def __repr__(self):
        return f'Time: {self.scheduled_time}'