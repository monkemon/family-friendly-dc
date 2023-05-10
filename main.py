import os
import discord

# load .env shit
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DC_TOKEN')
GUILD = os.getenv('DC_GUILD')

class CleverBot(discord.Client):
	commandChar = '+'	
	async def on_ready(self):
		print("Hello, there, i am ", self.user)

		# get your guild - stored in guild variable
		guild = discord.utils.get(self.guilds, name=GUILD)

		print(
			f'{self.user} is connected to the guild:'
			f'{guild.name} (id: {guild.id})'
		)
		print(guild.member_count, guild.members)
		for x in guild.members:
			print(x)
	
	async def on_message(self, message : discord.Message):
		if message.author == self.user:
			return

		await self.parse_message(message)

	async def on_error(event, *args, **kwargs):
		with open('err.log', 'a') as f:
			if event == 'on_message':
				f.write(f'Error in message: {args[0]}\n')
			else:
				raise

	async def parse_message(self, message : discord.Message):
		msg = message.content
		msg = msg.lstrip(' ')

		if (msg[0] != self.commandChar):
			return

		splitStart = msg.find(self.commandChar)
		splitEnd = msg.find(' ')
		if splitEnd < 0:
			splitEnd = len(msg)

		command = msg[splitStart + 1:splitEnd]
		text = msg[splitEnd + 1:]

		if command == 'spot':
			response = f"Searching '{text}' on Spotify..."
			await message.channel.send(response)

		if command == 'yt':
			response = f"Searching '{text}' on Youtub..."
			await message.channel.send(response)

		if command == 'exception':
			response = "Raising an exception"
			await message.channel.send(response)
			raise discord.DiscordException
		
		if command == 'kys':
			response = "kys yourself"
			await message.channel.send(response)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = CleverBot(intents=intents)
client.run(TOKEN)
