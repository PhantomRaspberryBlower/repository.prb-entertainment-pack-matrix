#!/usr/bin/env python

import sys                # Used to accept command-line argumengts
import getopt             # Used to parse command-line arguments

from config_settings import ConfigSettings

# Modify account_settings.ini with settings from kodi addon settings
def set_kodi_user_setting(path, section, name, value):
  conf_set = ConfigSettings(path)
  conf_set.get_value(section, name)
  conf_set.set_value(section, name, value)

output_path = ''
setting_section = ''
setting_name = ''
setting_value = ''

# Populate list of command-line argument values
argv = sys.argv[1:]
try:
  # Populate list of command-line arguments
  opts, args = getopt.getopt(argv, "p:s:n:v:",
                             ["path=",
                             "section=",
                             "name=",
                             "value="])
except:
  # Invalid command-line arguments - display valid options
  print('set_kodi_user_setting.py\n\t -p <path>\n\t -s <section>\n\t -n <name>\n\t'
        ' -v <value>\n')
  sys.exit()

# Parse command-line arguments if any and use to over-write kodi user settings
for opt, arg in opts:
  if opt == '--help':
    print('set_kodi_user_setting.py\n\t -p <path>\n\t -s <section>\n\t -n <name>\n\t'
          ' -v <value>\n')
    sys.exit()
  elif opt in ('-p', '--path'):
    output_path = arg
  elif opt in ('-s', '--section'):
    setting_section = arg
  elif opt in ('-n', '--name'):
    setting_name = arg
  elif opt in ('-v', '--value'):
    setting_value = arg

#try:
set_kodi_user_setting(output_path, setting_section, setting_name, setting_value)
#except:
#  print 'Something wicked happened :('
#  pass
