import discord
import asyncio
import random

import common



client = discord.Client( )
@client.event
async def on_ready( ):
	print( 'The Games Bot Online' )
	print( "Name: {}".format( client.user.name ) )
	print( "ID: {}".format( client.user.id ) )

@client.event
async def on_message( message ):
	if message.content.startswith( '!thisisgreat' ):
		await client.send_message( message.channel, 'Yeah!' )

	elif message.content.startswith( '!flip_coin' ):
		flip = random.choice( [ 'Heads', 'Tails' ] )
		await client.send_message( message.channel, flip )

	elif message.content.startswith( '!dice_roll' ):
		print( message )
		await client.send_message( message.channel, common.dice_roll( message.content[10: ] ) )



client.run( "NDA1MTUxODkzNjg2NTgzMjk3.DUgO5Q.CwHGFfE4c9xwExpa4cffvYC2hDs" )
