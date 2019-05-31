import discord
import asyncio
import random

import common
import config
import json

server_members = []

client = discord.Client( )
@client.event
async def on_ready( ):
	global server_members
	print( 'The Games Bot Online' )
	print( "Name: {}".format( client.user.name ) )
	print( "ID: {}".format( client.user.id ) )
	server_members = client.guilds[0].members

@client.event
async def on_message( message ):

	if message.author.bot == True:
		return

	#check if this is an actual command
	if message.content.startswith('!'):

		command = message.content[1:]
		command = command.lower()

		#check to see if this is a special mod only command
		if member_has_role(message.author, config.MOD_USER):
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

@client.event
async def on_raw_reaction_add( payload ):

	member = get_member_by_user_id( payload.user_id )

	if member.bot == False:
		with open( 'roles.json' ) as json_file:
			data = json.load( json_file )
			for i in data['roles']:
				if i['id'] == payload.message_id:
					role_obj = get_role_obj( i['role'] )
					await member_assign_role( member, role_obj )
					dm_message = "you have been added to the \"{}\" role in The_Games3 server".format( role_obj.name )
					await send_member_dm( member, dm_message)
					break


@client.event
async def on_raw_reaction_remove( payload ):

	member = get_member_by_user_id( payload.user_id )

	if member.bot == False:
		with open( 'roles.json' ) as json_file:
			data = json.load( json_file )
			for i in data['roles']:
				if i['id'] == payload.message_id:
					role_obj = get_role_obj( i['role'] )
					await member_remove_role( member, role_obj )
					dm_message = "you have been removed from the \"{}\" role in The_Games3 server".format( role_obj.name )
					await send_member_dm( member, dm_message)
					break


def get_member_by_user_id( user_id ):
	for member in server_members:
		if member.id == user_id:
			return member
	
	return None

async def member_assign_role( member, role ):
	if member_has_role(member, role.name) == False:
		await member.add_roles(role, reason = 'self assign role add')

async def member_remove_role( member, role ):
	if member_has_role(member, role.name) == True:
		await member.remove_roles(role, reason = 'self assign role removed')

def member_has_role( member, role ):
	if role.lower() in [x.name.lower() for x in member.roles]:
		return True

	return False


async def send_member_dm( member, message ):
	dm_channel = member.dm_channel
	if dm_channel == None:
		await member.create_dm()
		dm_channel = member.dm_channel
	await dm_channel.send( message )
	

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

	return emoji


async def show_roles( message ):

	with open('roles.json', 'r+') as json_file:
		data = json.load(json_file)
		for i in data['roles']:
			role_obj = get_role_obj(i['role'])
			if role_obj != None:
				emoji = get_emoji_obj(i['emoji'])
				output = 'React with {} to be assigned {}\n{}\n'.format(emoji,role_obj.mention, i['description'])
				msg = await message.channel.send( output )
				await msg.add_reaction(emoji)
				#save the message ID to the roles.json file
				i['id'] = msg.id

		#write any updated message ID's to the roles file
		json_file.seek(0)
		json.dump(data, json_file, sort_keys=True, indent=3, separators=(',', ': '))
		json_file.truncate()

client.run( config.BOT_ID )
