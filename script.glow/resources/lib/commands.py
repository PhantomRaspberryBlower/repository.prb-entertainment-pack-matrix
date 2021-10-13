import sys                # Used to accept command-line argumengts
import getopt             # Used to parse command-line arguments
import urlparse           # Used to parse url
from imap_glow import ImapGlow

message = ''              # Stores the message to broadcast using UDP

# Populate list of command-line argument values
argv = sys.argv[1:]

try:
  # Populate list of command-line arguments
  opts, args = getopt.getopt(argv, "m:", ["message="])
  # Parse command-line arguments if any and use to over-write kodi user settings
  for opt, arg in opts:
    if opt in ('-m', '--message'):
      message = arg
  glow = ImapGlow()
  print message
  glow.send(message)
except:
  # Invalid command-line arguments - display valid options
  sys.exit()

