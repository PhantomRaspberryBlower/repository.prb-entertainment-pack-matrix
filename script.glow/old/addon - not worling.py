import sys                # Used to accept command-line argumengts
import getopt             # Used to parse command-line arguments
import urlparse           # Used to parse url

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

if action != None:
  issue_command(action)