import asyncio, aiohttp, discord, os, re

class FrostCleverbot(discord.Client):
    async def on_ready(self):
        print('Logged in as {0.user.name} (ID: {0.user.id}) | {1} servers'.format(self, str(len(self.guilds))))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("chat with me!"))

    async def on_message(self, message):
        if not message.author.bot and (not message.guild or message.guild.me in message.mentions):
            async with message.channel.typing():
            try:
                input = re.sub('<@!?'+str(self.user.id)+'>', '', message.content).strip()
                params = {'botid': os.environ['PANDORA_BOT'] or 'PANDORABOTS BOT ID HERE', 'custid': message.author.id, 'input': input or 'Hello'}
                async with http.get('https://www.pandorabots.com/pandora/talk-xml', params=params) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        text = text[text.find('<that>')+6:text.rfind('</that>')]
                        text = text.replace('&quot;','"').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('<br>',' ')
                        await message.channel.send(text)
                    else:
                        await message.channel.send('Uh oh, I didn\'t quite catch that!')
            except asyncio.TimeoutError:
                await message.channel.send('Uh oh, I think my head is on backwards!')

print('Starting...')
http = aiohttp.ClientSession()
FrostCleverbot().run(os.environ['BOT_TOKEN'] or 'PUT DISCORD BOT TOKEN HERE')
