"""
Common comands used by the bot
"""
import random
import re
import string

def dice_roll( message ):
    rand_int = [ ]
    requested_role = message.split( 'd' )
    error_msg = "This is not a valid dice range"
    if len(requested_role) > 1:
        dices = int( requested_role[ 0 ] )
        dice_type = int( requested_role[ 1 ] )
        if dices not in range(1, 21):
            return error_msg
        if dice_type not in range(2, 21):
            return error_msg

        for d in range( dices ):
            rand_int.append( random.randint( 0, dice_type ) )
        
        return str( rand_int )
    else:
        return error_msg


def ope_finder( message ):
    ope = re.findall( r'(ope)', message, re.I )
    if ope:
        return True
    else:
        return False
