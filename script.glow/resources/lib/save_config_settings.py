#!/usr/bin/env python

import sys                # Used to accept command-line argumengts
import getopt             # Used to parse command-line arguments

import thread
from kodi_user_settings import KodiUserSettings
from imap_glow import ImapGlow

# Declare variables
# Constants

RED_LED_PIN = 12
GREEN_LED_PIN = 16
BLUE_LED_PIN = 18
USER_SETTINGS_PATH = '/home/pi/python_scripts/glow/account_settings.ini'
KODI_USER_SETTINGS_PATH = '/home/pi/.kodi/userdata/addon_data/settings.xml'

# KodiUserSettings(USER_SETTINGS_PATH, KODI_USER_SETTINGS_PATH)

glow = ImapGlow(RED_LED_PIN, GREEN_LED_PIN, BLUE_LED_PIN, USER_SETTINGS_PATH)

try:
#  glow.start(True)
  thread.start_new_thread(glow.start, (False,))
  while True:
    pass
except KeyboardInterrupt:
  import time
  glow.stop()
  print 'wait...'
  time.sleep(32)
