import os
import discord
import csv

def add_task(author, tsk):
  with open('tasks.csv', 'a') as tasks:
    writer = csv.writer(tasks)
    writer.writerow([author] + tsk)

deleted_rows = []
def remove_task(username, task_name):
  with open('tasks.csv', 'r') as tasks:
    file = csv.reader(tasks)
    idx = 0
    for row in file:
      if row[0] == username and row[1] == task_name and idx not in deleted_rows:
        break
      idx += 1
  deleted_rows.append(idx)        
   
def todo(author):
  #returns all tasks and when they are due
  with open('tasks.csv', 'r') as tasks:
    temp = ''
    csv_reader = csv.reader(tasks, delimiter=',')
    count = 1
    idx = 0
    for row in csv_reader:
      if row[0] == author and idx not in deleted_rows:
        temp += ("Task " + str(count) + ": "  + ', '.join(row[1:]) + '\n')
        count += 1
      idx += 1
    temp = '`'+author+'`'+"'s to-do list:\n\n" + temp
    return temp
  
client = discord.Client(intents = discord.Intents.default())

@client.event
async def on_message(message):    
    
  if message.author != client.user: # detects all messages sent by users

    if client.user.mentioned_in(message): # commands to the bot (messages mentioning bot)
      actual_contents = message.content[23:] # message not including prefix
      contents_list = actual_contents.split(', ') # list of things
      message_author = str(message.author)
      command = contents_list[0] # command given to bot
      if command == 'info': # info on how to use bot
        response = "Task Bot is a discord bot that increases productivity.\n\n\
Prefix: `@Task_Bot`\n\n\
Commands:\n\
`info`: sends the user info on how to use Task_Bot\n\
`add task`: adds a task to the user's todo list\n\
`remove task`: removes a task if you are done with it\n\
`say hi`: says hi\n\
`to dos`: get all your tasks to do\n\
Add task command syntax: `@Task_Bot <command>, <task name>, <start date>, <due date>, <additional notes>`\n\
Example of an add task command: `@Task_Bot add task, study for sat, 3/18/23, 7/3/98, i dont want to do this`"
        await message.channel.send(response)
       
      if command == 'add task':
        add_task(message_author, contents_list[1:])
        await message.channel.send('Added ' + '`'+contents_list[1]+'`')
      
      if command == 'say hi':
        await message.channel.send('wassup')
        
      if command == 'remove task':
        task_name = contents_list[1]
        remove_task(message_author, task_name)
        await message.channel.send('Removed ' + '`'+contents_list[1]+'`')
      if command == 'to dos':
        y = todo(message_author)
        await message.channel.send(y)
        
my_secret = os.environ['TOKEN']
client.run(my_secret)

