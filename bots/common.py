"""
Common comands used by the bot
"""
import random
import re
import string

def dice_roll( message ):
    rand_int = [ ]
    requested_dice = message.split( 'd' )
    dices = int( requested_dice[ 0 ] )
    dice_type = int( requested_dice[ 1 ] )

    for d in range( dices ):
        rand_int.append( random.randint( 0, dice_type ) )
    
    return str( rand_int )


def ope_finder( message ):
    ope = re.findall( r'(ope)\w+', message, re.I )
    if ope:
        print( 'Found.' )
    else:
        print( "There's something very wrong!" )
