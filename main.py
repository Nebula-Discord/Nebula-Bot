import discord
import os
import requests
import random
import json
from replit import db
#starts discord
client = discord.Client()

#variables
sad_words = ['sad', 'depressed', 'unhappy']
starter_encouragements = ['cheer up', 'it will get bertter', 'your amazing']

#contacts database
def update_encouragements(message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(message)
    db["encouragements"] = encouragements
  else:
    db['encouragements'] = [message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

#random quote string
def random_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = 'The power of ' + json_data[0]['q'] + ' fills you with determination'" -" + json_data[0]['a']
  return(quote)

#daily quote string
def daily_quote():
  response = requests.get("https://zenquotes.io/api/today")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#prints to theconsole when the bot is ready
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


#IMPORTANT commands go here
@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return

    
  #random quote command
  if message.content.startswith('$quote'):
    quote = random_quote()
    await message.channel.send(quote)

  #daily quote command
  if message.content.startswith('$dailyquote'):
    quote = daily_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options.extend(db["encouragements"])

  #encouragemnets
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith('$new'):
    encouraging_message = msg.split('$new ',1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send('Added!')

  if msg.startswith('$del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('$del ',1)[1])
      delete_encouragement(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)
    

client.run(os.getenv('TOKEN'))