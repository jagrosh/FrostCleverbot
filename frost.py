import discord
import asyncio
import re
from cleverbot import Cleverbot

client = discord.Client()
cb = Cleverbot()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(str(len(client.servers))+' servers')
    await client.change_status(game=discord.Game(name='chat with me!'),idle=False)

@client.event
async def on_message(message):
    if not message.author.id == client.user.id:
        if message.server == None:
            await client.send_typing(message.channel)
            await client.send_message(message.channel, cb.ask(message.content))
        else:
            m = re.match(r'(.*)\s*<@!?'+client.user.id+'>\s*(.*)',message.content)
            if m != None:
                await client.send_typing(message.channel)
                await client.send_message(message.channel, cb.ask(m.group(1)+' '+m.group(2)))

print('Starting...')
client.run('YOUR TOKEN HERE')
