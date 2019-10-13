##########################################################
#                                                        #
#                 ¡ This is a template !                 #
#                                                        #
#   Make sure to edit it with your preferred settings!   #
#    And to place it in the root of the bot's folder,    #
#        without the 'template_' part of the name        #
#                                                        #
##########################################################
"""
Settings and options for the bot.
---
"""

# The prefix for the bot (str). Define a list of stings for multiple prefixes.
# ie: `["?", "!", "pls "]`
PREFIX = "?"

# Whether the bot should print full stacktraces for normal exceptions: `True`,
# or be nice and only print small messages: `False` (the default).
DEBUG = False

# A tuple of user IDs that should be considered "bot owners".
# * Those users will have full control over the bot.
# ! This MUST be a tuple of integers. Single element tuple: `(123,)`
OWNERS_UIDS = (200102491231092736,)

# The cogs to load when running the bot.
COGS = ['basecog', 'morsecog', 'funcog', 'gridcog', 'hamcog', 'imagecog',
        'studycog', 'ae7qcog']

# The text to put in the "playing" status.
GAME = 'with lids on 7.200'
