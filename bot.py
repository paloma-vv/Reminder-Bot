# bot to countdown to end of class and notify students
# Checks the countdowns dictionary every minute to see if any countdowns are ready to be notified
# If so, it notifies the channel the countdown was added in

import os
countdowns = {}
import discord
import asyncio
import datetime
from keep_alive import keep_alive
keep_alive()

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    print(message)
    if msg.startswith("$add"):
        contents = msg.split()
        if len(contents) != 7:
            await message.channel.send("Invalid command. Try $add [name] [day_of_week] [time_start] [time_end] [interval] [last_day]", silent=True)
            return
        name = contents[1]
        day = contents[2]
        time_start = contents[3]
        time_end = contents[4]
        interval = contents[5]
        last_day = contents[6]
        countdowns[name] = [day, time_start, time_end, interval, last_day, message.channel]
        await message.channel.send("Added " + name + " to countdowns.", silent=True)

    

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def check_countdowns():
    #example command to add a countdown from user input in discord: $add math monday 09:00 10:00 1 2020-12-03
    while True:
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M"))
 
        for name in countdowns:
            day = countdowns[name][0]
            time_start = countdowns[name][1]
            time_end = countdowns[name][2]
            interval = int(countdowns[name][3])
            last_day = countdowns[name][4]
            channel = countdowns[name][5]
            length_of_class = datetime.datetime.strptime(time_end, "%H:%M") - datetime.datetime.strptime(time_start, "%H:%M")

            if day == now.strftime("%A").lower() and now.strftime("%H:%M") == time_start:
                await channel.send("Class " + name + " has started.", silent=True)
            if day == now.strftime("%A").lower() and now.strftime("%H:%M") == time_end:
                await channel.send("Class " + name + " has ended.", silent=True)
                
            # if current time is between start and end time
            if day == now.strftime("%A").lower() and now.strftime("%H:%M") > datetime.datetime.strptime(time_start, "%H:%M").strftime("%H:%M") and now.strftime("%H:%M") < datetime.datetime.strptime(time_end, "%H:%M").strftime("%H:%M"):
                # if time_left_in_clas % interval == 0, notify
                time_left_in_class_datetime = datetime.datetime.strptime(time_end, "%H:%M") - datetime.datetime.strptime(now.strftime("%H:%M"), "%H:%M")
                time_left_in_class = time_left_in_class_datetime.seconds // 60
                if time_left_in_class % interval == 0:
                    await channel.send("Class " + name + " has " + str(time_left_in_class) + " minutes left.", silent=True)
                    
                

            
            # if it is the day after the last day, delete the countdown
            if now.strftime("%Y-%m-%d") == last_day:
                del countdowns[name]
                await channel.send("Class " + name + " has ended.", silent=True)



        await asyncio.sleep(60)

        

async def main():
    asyncio.create_task(check_countdowns())
    await client.start(os.environ.get('token'))

asyncio.run(main())
        
client.run(os.environ.get('token'))
