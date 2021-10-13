import sys                # Used to accept command-line argumengts
import getopt             # Used to parse command-line arguments
import urlparse           # Used to parse url

from resources.lib.imap_glow import ImapGlow

#SCRIPT_PATH = 'sudo python /home/osmc/.kodi/addons/script.imap-glow/resources/lib/user_setting.py'
SCRIPT_PATH = 'sudo python special://home/addons/script.imap-glow/resources/lib/user_setting.py'
message = ''

# Define the following commands:- start, stop, poweroff, settings, test_email, 

def issue_command(command):
   subprocess.call(SCRIPT_PATH + ' ' + command, shell=True)
   sys.exit()            ### Not sure if I need this line !!!
   argv = ['-m', command]

try:
    params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
    action = params['message']
except:
    action = None

if action == None:
  # Populate list of command-line argument values
  argv = sys.argv[1:]
else:
  issue_command(action)

try:
  # Populate list of command-line arguments
  opts, args = getopt.getopt(argv, "m:", ["message="])
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