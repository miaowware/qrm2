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
prefix = ["? ", "?"]

# The prefix to use for display purposes (ex: status message).
display_prefix = "?"

# Whether the bot should print full stacktraces for normal exceptions: `True`,
# or be nice and only print small messages: `False` (the default).
debug = False

# A tuple of user IDs that should be considered "bot owners".
# * Those users will have full control over the bot.
# ! This MUST be a tuple of integers. Single element tuple: `(123,)`
owners_uids = (200102491231092736, 564766093051166729)

# The extensions to load when running the bot.
exts = [
    "ae7q",
    "base",
    "fun",
    "grid",
    "ham",
    "image",
    "lookup",
    "morse",
    "qrz",
    "study",
    "tex",
    "weather",
    "dbconv",
    "propagation",
]

# URL to the resources
resources_url = "https://qrmresources.miaow.io/resources/"

# If True (default): when doing QRZ callsign lookups, show the nickname in place of the first name, if it exists
# if False: use QRZ's default name format
qrz_only_nickname = True

# enable a command that provides a link to add the bot to a server
enable_invite_cmd = True

# the default permissions for the bot, to be included in the invite link for ?invite
# this probably does not need to be changed
invite_perms = 67488832

# Either "time", "random", or "fixed" (first item in statuses)
status_mode = "fixed"

# Random statuses pool
statuses = ["with lids on the air", "with fire"]

# Timezone for the status (string)
# See https://pythonhosted.org/pytz/ for more info
status_tz = "US/Eastern"

# The text to put in the "playing" status, with start and stop times
time_statuses = [("with lids on 3.840", (00, 00), (6, 00)),
                 ("with lids on 7.200", (6, 00), (10, 00)),
                 ("with lids on 14.313", (10, 00), (18, 00)),
                 ("with lids on 7.200", (18, 00), (20, 00)),
                 ("with lids on 3.840", (20, 00), (23, 59))]

# append " | {display_prefix}help" to the Discord playing status
show_help = False

# Emoji IDs and keywords for emoji reactions
# Use the format {emoji_id (int): ("tuple", "of", "lowercase", "keywords")}
msg_reacts = {}

# A :pika: emote's ID, None for no emote :c
pika = 658733876176355338

# Base URL to a deployment of rTeX, which performs LaTeX rendering.
rtex_instance = "https://rtex.probablyaweb.site/"
