##########################################################
#                                                        #
#                 ¡ This is a template !                 #
#                                                        #
#   Make sure to edit it with your preferred settings!   #
#              And to place it in the /data              #
#                subdirectory of the bot,                #
#        without the 'template_' part of the name        #
#                                                        #
##########################################################
"""
Settings and options for the bot.
---
"""

# The prefix for the bot (str). Define a list of stings for multiple prefixes.
# ie: `["?", "!", "pls "]`
prefix = "?"

# Whether the bot should print full stacktraces for normal exceptions: `True`,
# or be nice and only print small messages: `False` (the default).
debug = False

# A tuple of user IDs that should be considered "bot owners".
# * Those users will have full control over the bot.
# ! This MUST be a tuple of integers. Single element tuple: `(123,)`
owners_uids = (200102491231092736,)

# The extensions to load when running the bot.
exts = ['ae7q', 'base', 'fun', 'grid', 'ham', 'image', 'lookup', 'morse', 'qrz', 'study', 'weather']

# The text to put in the "playing" status.
game = 'with lids on 7.200'

# Emoji IDs and keywords for emoji reactions
# Use the format {emoji_id (int): ('tuple', 'of', 'lowercase', 'keywords')}
msg_reacts = {}
