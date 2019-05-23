import discord
import asyncio
import random

import common
import config


client = discord.Client( )
@client.event
async def on_ready( ):
	print( 'The Games Bot Online' )
	print( "Name: {}".format( client.user.name ) )
	print( "ID: {}".format( client.user.id ) )

@client.event
async def on_message( message ):

	#check if this is an actual command
	if message.content.startswith('!'):

		command = message.content[1:]
		command = command.lower()

		if command.startswith( 'thisisgreat' ):
			await message.channel.send( 'Yeah!' )

		elif command.startswith( 'flip_coin' ):
			flip = random.choice( [ 'Heads', 'Tails' ] )
			await message.channel.send( flip )

		elif command.startswith( 'dice_roll' ):
			#print( message )
			await message.channel.send( common.dice_roll( command.split()[1] ) )



client.run( config.BOT_ID )
