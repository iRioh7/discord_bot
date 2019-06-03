import discord
import asyncio
import random
import adjustables_testing
import adjustables

import common
import config
import json

SERVER_MEMBERS = []
TESTING = True
MOD_USER = None
COMMAND_MARKER = "!"
ROLES_FILE = ""
BOT_ID = ""

MOD_USER = config.MOD_USER
if TESTING == True:
	BOT_ID = config.TEST_BOT_ID
	COMMAND_MARKER = adjustables_testing.COMMAND_MARKER
	ROLES_FILE = adjustables_testing.ROLES_FILE
else:
	BOT_ID = config.BOT_ID
	COMMAND_MARKER = adjustables.COMMAND_MARKER
	ROLES_FILE = adjustables.ROLES_FILE

client = discord.Client( )
@client.event
async def on_ready( ):
	global SERVER_MEMBERS
	print( 'The Games Bot Online' )
	print( "Name: {}".format( client.user.name ) )
	print( "ID: {}".format( client.user.id ) )
	SERVER_MEMBERS = client.guilds[0].members

	

@client.event
async def on_message( message ):

	if message.author.bot == True:
		return

	#check if this is an actual command
	if message.content.startswith(COMMAND_MARKER):

		command = message.content[1:]
		command = command.lower()

		#check to see if this is a special mod only command
		if member_has_role(message.author, MOD_USER):
			if command.startswith( 'show_roles' ):
				await show_roles(message)
			elif command.startswith( 'update_roles' ):
				await update_roles(message)
		
		if command.startswith( 'thisisgreat' ):
			await message.channel.send( 'Yeah!' )

		elif command.startswith( 'flip_coin' ):
			flip = random.choice( [ 'Heads', 'Tails' ] )
			await message.channel.send( flip )

		elif command.startswith( 'dice_roll' ):
			parameters = command.split()
			if len(parameters) > 1:
				await message.channel.send( common.dice_roll( parameters[1] ) )
			else:
				await message.channel.send( "You need to specify the dice to roll" )

	if common.ope_finder( message.content ):
		emoji = get_emoji_obj( 'OPE' )
		await message.add_reaction( emoji )

@client.event
async def on_raw_reaction_add( payload ):

	member = get_member_by_user_id( payload.user_id )

	if member.bot == False:
		with open( ROLES_FILE ) as json_file:
			data = json.load( json_file )
			for i in data['roles']:
				emoji = get_emoji_obj( i['emoji'] )
				if i['id'] == payload.message_id and emoji.id == payload.emoji.id: #make sure we are reacting with the correct emoji
					role_obj = get_role_obj( i['role'] )
					await member_assign_role( member, role_obj )
					# if 'updated' in i:
					# 	channel_obj = get_channel_by_id( payload.channel_id )
					# 	msg = await channel_obj.fetch_message(i['id'])
					# 	output = 'React with {} to be assigned {}\n{}\n'.format(emoji,role_obj.mention, i['description'])
					# 	await msg.edit(content = output)
					# 	await msg.add_reaction(emoji)
						#await channel_obj.send( "found message {}".format(i['id']) )
					break


@client.event
async def on_raw_reaction_remove( payload ):

	member = get_member_by_user_id( payload.user_id )

	if member.bot == False:
		with open( ROLES_FILE ) as json_file:
			data = json.load( json_file )
			for i in data['roles']:
				emoji = get_emoji_obj( i['emoji'] )
				if i['id'] == payload.message_id and emoji.id == payload.emoji.id:
					role_obj = get_role_obj( i['role'] )
					await member_remove_role( member, role_obj )
					break


def get_member_by_user_id( user_id ):
	for member in SERVER_MEMBERS:
		if member.id == user_id:
			return member
	
	return None

def get_channel_by_id( channel_id ):
	for channel in client.guilds[0].channels:
		if channel.id == channel_id:
			return channel

	return None

async def member_assign_role( member, role ):
	if member_has_role(member, role.name) == False:
		await member.add_roles(role, reason = 'self assign role add')
		dm_message = "you have been added to the \"{}\" role in The_Games3 server".format( role.name )
		await send_member_dm( member, dm_message)

async def member_remove_role( member, role ):
	if member_has_role(member, role.name) == True:
		await member.remove_roles(role, reason = 'self assign role removed')
		dm_message = "you have been removed from the \"{}\" role in The_Games3 server".format( role.name )
		await send_member_dm( member, dm_message)

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


def format_role_message(emoji_obj, role_obj, description):
	return 'React with {} to be assigned {}\n{}\n'.format(emoji_obj, role_obj.mention, description)


async def show_roles( message ):

	with open(ROLES_FILE, 'r+') as json_file:
		data = json.load(json_file)
		for i in data['roles']:
			role_obj = get_role_obj(i['role'])
			if role_obj != None:
				emoji = get_emoji_obj(i['emoji'])
				output = format_role_message(emoji, role_obj, i['description'])
				msg = await message.channel.send( output )
				await msg.add_reaction(emoji)
				#save the message ID to the roles.json file
				i['id'] = msg.id

		#write any updated message ID's to the roles file
		json_file.seek(0)
		json.dump(data, json_file, sort_keys=True, indent=3, separators=(',', ': '))
		json_file.truncate()

async def update_roles( message ):

	with open( ROLES_FILE, 'r+' ) as json_file:
		data = json.load(json_file)
		updated = False
		for i in data['roles']:
			if i['id'] != None and 'updated' in i:
				updated = True
				emoji = get_emoji_obj(i['emoji'])
				output = format_role_message(emoji, get_role_obj(i['role']), i['description'])
				msg = await message.channel.fetch_message(i['id'])
				await msg.edit(content = output)
				await msg.add_reaction(emoji)
				del i['updated'] #remove the updated marker

		if updated:
			#write any updated markers to the roles file
			json_file.seek(0)
			json.dump(data, json_file, sort_keys=True, indent=3, separators=(',', ': '))
			json_file.truncate()

client.run( BOT_ID )