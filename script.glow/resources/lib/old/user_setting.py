import sys                # Used to accept command-line argumengts
import getopt             # Used to parse command-line arguments

from imap_glow import ImapGlow

# Populate list of command-line argument values
argv = sys.argv[1:]
print argv
try:
  # Populate list of command-line arguments
  opts, args = getopt.getopt(argv, "m:",
                             ["message="])
except:
  # Invalid command-line arguments - display valid options
  print('user_setting.py\n\t -m <message>\n')
  sys.exit()

# Parse command-line arguments if any and use to over-write kodi user settings
for opt, arg in opts:
  if opt == '--help':
    print('user_setting.py\n\t -m <message>\n')
    sys.exit()
  elif opt in ('-m', '--message'):
    message = arg
glow = ImapGlow()
glow.send(message)