import discord
import os
import requests
import random
import json

client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy']

starter_encouragements = ['cheer up', 'it will get bertter', 'your amazing']

def random_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def daily_quote():
  response = requests.get("https://zenquotes.io/api/today")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return

    

  if message.content.startswith('$quote'):
    quote = random_quote()
    await message.channel.send(quote)

  if message.content.startswith('$dailyquote'):
    quote = daily_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

#@client.event
#async def on_message(message):
#  if message.author == client.user:
#    return
#
#  if message.content.startswith('$dailyquote'):
#    quote = daily_quote()
#    await message.channel.send(quote)

client.run(os.getenv('TOKEN'))