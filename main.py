import os
import discord
import requests
import tokenService

from countryFlags import country_flags

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
			if text == "":
				response = f"Please enter some query"
				await message.channel.send(response)
				return

			response = f"Searching '{text}' on Spotify..."
			await message.channel.send(response)
			searchresp = await self.spotifySearch(text)
			text = '\n'.join(searchresp)
			await message.channel.send(text)

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

	async def spotifySearch(self, query: str):
		tok = self.read_token()
		if len(tok) == 0:
			tok = tokenService.get_token(os.getenv('SPOT_USER'), os.getenv('SPOT_SECRET'))
			self.write_token(tok)

		baseUrl = 'https://api.spotify.com/v1/search'
		search = query.replace(' ', '+')
		auth = {'Authorization' : 'Bearer ' + tok}
		url = baseUrl + '?q=' + search + '&type=track&limit=1'
		resp = requests.get(url=url, headers=auth)

		if resp.status_code  == 401:
			token = tokenService.get_token(os.getenv('SPOT_USER'), os.getenv('SPOT_SECRET'))
			self.write_token(token)

			auth = {'Authorization' : 'Bearer ' + tok}
			resp = requests.get(url=url, headers=auth)

		tracks = resp.json()
		tracks = tracks['tracks']
		if tracks['total'] == 0:
			return 'Nothing found'
		
		track = tracks['items'][0]

		lines = []
		lines.append(f"{track['name']}")
		lines.append(f"Album: {track['album']['name']}")
		lines.append(f"Disc: {track['disc_number']}")
		lines.append(f"Length: {track['duration_ms']}ms")
		lines.append(f"Actual popularity: {track['popularity']}")
		lines.append(f"Track number: {track['track_number']}")
		lines.append(f"Spotify ID: {track['id']}")

		id = track['uri'].split(':')
		print(id)
		id = f"https://open.spotify.com/track/{id[2]}"
		lines.append(f"Track url: {id}")
		lines.append(f"Track API href: {track['href']}")
		lines.append(f"Is explicit: {track['explicit']}")

		countrys = [country_flags[flagCode] for flagCode in track['available_markets']]
		lines.append(f"Available in: {countrys}")

		return lines
	
	def write_token(self, token):
		with open('token', 'w') as file:
			file.write(token)
	
	def read_token(self):
		if os.path.exists('./token') == False:
			self.write_token("")

		ret = ""
		with open('token', 'r') as file:
			ret = file.read()
		return ret


		



intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = CleverBot(intents=intents)
client.run(TOKEN)


