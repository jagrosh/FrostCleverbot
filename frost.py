import asyncio
import aiohttp
import json
import discord

client = discord.Client()
user = 'CLEVERBOT.IO API USER'
key = 'CLEVERBOT.IO API KEY'

client.session = aiohttp.ClientSession()
client.ready = False

@client.event
async def on_ready():
    print('Starting...')
    payload = {'data': json.dumps({'user': user,
                                   'key': key,
                                   'nick': client.user.name}),
               'headers': {'content-type': 'application/json'}}
    async with client.session.post(r'https://cleverbot.io/1.0/create', **payload) as r:
        j = await r.json()
        if j['status'] != 'success':
            print('Something went wrong with cleverbot.io login!')
            print(j['status'])
            client.session.close()
            return await client.logout()
    print('Logged into cleverbot.io successfully!')
    client.ready = True
    print('Logged in as {0.user.name} (ID: {0.user.id} ) | {1} servers'
          .format(client, str(len(client.servers))))
    await client.change_presence(game=discord.Game(name='chat with me!'))


@client.event
async def on_message(message):
    if not client.ready or message.author.bot:
        return
    if not message.server or client.user in message.mentions:
        await client.send_typing(message.channel)
        text = message.content.replace(client.user.mention, '')
        payload = {'data': json.dumps({'user': user,
                                       'key': key,
                                       'text': text,
                                       'nick': client.user.name}),
                   'headers': {'content-type': 'application/json'},
                   'timeout':10}
        try:
            async with client.session.post(r'https://cleverbot.io/1.0/ask', **payload) as r:
                if r.status == 200:
                    j = await r.json()
                    if j['status'] == 'success':
                        print(j['response'])
                        await client.send_message(message.channel, j['response'])
        except asyncio.TimeoutError:
            await client.send_message(message.channel, 'Request timed out!')


client.run('DISCORD BOT TOKEN')
