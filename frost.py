import discord
import asyncio
import requests
import json

client = discord.Client()
user = 'CLEVERBOT.IO API USER'
key = 'CLEVERBOT.IO API KEY'

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+str(client.user.id)+') | '+str(len(client.guilds))+' servers')
    await client.change_presence(game=discord.Game(name='chat with me!'))

@client.event
async def on_message(message):
    if not message.author.bot and (message.guild == None or client.user in message.mentions):
        await message.channel.trigger_typing()
        txt = message.content.replace(message.guild.me.mention,'') if message.guild else message.content
        r = json.loads(requests.post('https://cleverbot.io/1.0/ask', json={'user':user, 'key':key, 'nick':'frost', 'text':txt}).text)
        if r['status'] == 'success':
            await message.channel.send(r['response'] )

print('Starting...')
requests.post('https://cleverbot.io/1.0/create', json={'user':user, 'key':key, 'nick':'frost'})
client.run('DISCORD BOT TOKEN')
