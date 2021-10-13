import sys                # Used to accept command-line argumengts
import getopt             # Used to parse command-line arguments

from resources.lib.imap_glow import ImapGlow

import urlparse,sys

message = ''

try:
    params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
    action = params['message']
except:
    action = None

if action == None:
  # Populate list of command-line argument values
  argv = sys.argv[1:]
elif action == 'start':
   import subprocess
   subprocess.call('sudo python /home/osmc/.kodi/addons/script.imap-glow/resources/lib/user_setting.py -m start', shell=True)
   sys.exit()
   argv = ['-m', 'start']
elif action == 'stop':
   import subprocess
   subprocess.call('sudo python /home/osmc/.kodi/addons/script.imap-glow/resources/lib/user_setting.py -m stop', shell=True)
   sys.exit()
   argv = ['-m', 'stop']
elif action == 'poweroff':
   import subprocess
   subprocess.call('sudo python /home/osmc/.kodi/addons/script.imap-glow/resources/lib/user_setting.py -m poweroff', shell=True)
   sys.exit()
   argv = ['-m', 'poweroff']

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
    print message
glow = ImapGlow()
glow.send(message)