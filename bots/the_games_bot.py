import discord
import asyncio
import random

import common
import config
import json


client = discord.Client( )
@client.event
async def on_ready( ):
	print( 'The Games Bot Online' )
	print( "Name: {}".format( client.user.name ) )
	print( "ID: {}".format( client.user.id ) )

@client.event
async def on_message( message ):

	if message.author.bot == True:
		return

	#check if this is an actual command
	if message.content.startswith('!'):

		command = message.content[1:]
		command = command.lower()

		#check to see if this is a special mod only command
		if user_has_role(message.author, config.MOD_USER):
			if command.startswith( 'show_roles' ):
				await show_roles(message)
		
		if command.startswith( 'thisisgreat' ):
			await message.channel.send( 'Yeah!' )

		elif command.startswith( 'flip_coin' ):
			flip = random.choice( [ 'Heads', 'Tails' ] )
			await message.channel.send( flip )

		elif command.startswith( 'dice_roll' ):
			#print( message )
			await message.channel.send( common.dice_roll( command.split()[1] ) )


def user_has_role( user, role ):
	if role.lower() in [x.name.lower() for x in user.roles]:
		return True

	return False

def get_role_obj( role ):
	guild_obj = client.guilds[0]
	for x in guild_obj.roles:
		if x.name.lower() == role.lower():
			return x
	return None

def get_emoji_obj( emoji ):
	guild_obj = client.guilds[0]
	for x in guild_obj.emojis:
		if x.name.lower() == emoji.lower():
			return x

	return None


async def show_roles( message ):

	with open('roles.json') as json_file:
		data = json.load(json_file)
		for i in data['roles']:
			role_obj = get_role_obj(i['role'])
			if role_obj != None:
				output = '{}\n{}\n'.format(role_obj.mention, i['description'])
				msg = await message.channel.send( output )
				emoji = get_emoji_obj(i['emoji'])
				await msg.add_reaction(emoji)



client.run( config.BOT_ID )
