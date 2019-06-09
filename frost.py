import asyncio, aiohttp, discord, os, re

class FrostCleverbot(discord.Client):
    async def on_ready(self):
        print('Logged in as {0.user.name} (ID: {0.user.id} ) | {1} servers'.format(self, str(len(self.servers))))
        await self.change_presence(game=discord.Game(name='chat with me!'))

    async def on_message(self, message):
        if not message.author.bot and (not message.server or message.server.me in message.mentions):
            await self.send_typing(message.channel)
            try:
                input = re.sub('<@!?'+self.user.id+'>', '', message.content).strip()
                params = {'botid': os.environ['PANDORA_BOT'] or 'PANDORABOTS BOT ID HERE', 'custid': message.author.id, 'input': input or 'Hello'}
                async with http.get('https://www.pandorabots.com/pandora/talk-xml', params=params) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        text = text[text.find('<that>')+6:text.rfind('</that>')]
                        text = text.replace('&quot;','"').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('<br>',' ')
                        await self.send_message(message.channel, text)
                    else:
                        await self.send_message(message.channel, 'Uh oh, I didn\'t quite catch that!')
            except asyncio.TimeoutError:
                await self.send_message(message.channel, 'Uh oh, I think my head is on backwards!')

print('Starting...')
http = aiohttp.ClientSession()
FrostCleverbot().run(os.environ['BOT_TOKEN'] or 'PUT DISCORD BOT TOKEN HERE')