import discord
import asyncio
from cleverbot import Cleverbot

client = discord.Client()
cb = Cleverbot('frost discord bot')

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+')')
    print(str(len(client.servers))+' servers')
    await client.change_presence(game=discord.Game(name='chat with me!'))

@client.event
async def on_message(message):
    if not message.author.bot:
        if message.server == None:
            await client.send_typing(message.channel)
            await client.send_message(message.channel, cb.ask(message.content) )
        elif client.user in message.mentions:
            await client.send_typing(message.channel)
            await client.send_message(message.channel, cb.ask(message.content.replace(message.server.me.mention, '')) )

print('Starting...')
client.run('YOUR TOKEN HERE')
