#!/usr/bin/env python

# PRB Imap Glow (Security Pack)
# Connects to IMAP server looking for specific emails
# and lights up the candle in one of seven colours then
# flashes to represent the number of unread emails.
# for example all work related emails could be red
# whilst family and friends could light up green.

# Date: 01 March 2016
# Written By: Phantom Raspberry Blower

import xbmcaddon, xbmc, xbmcgui
import thread
from resources.lib.imap_glow import ImapGlow
import os
import sys

# potential better way
# from subprocess import call(["ls", "-l"])

__addon__ = xbmcaddon.Addon(id='script.imap-glow')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__author__ = "Phantom Raspberry Blower"

ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10 
ACTION_NAV_BACK = 92

class ImapGlowAddon(xbmcgui.Window):
  # Initilize the class
  def __init__(self):
    self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    # Background Image
    self.window.setProperty('MyAddonIsRunning', 'true')
    self.addControl(xbmcgui.ControlImage(0, 0, 1280, 720, 'special://home/addons/script.imap-glow/background.jpg'))
    # Display Press HOME to exit
    self.lExit = xbmcgui.ControlLabel(470, 25, 800, 200, '', 'font16', '0xFF868784', )
    self.addControl(self.lExit)
    self.lExit.setLabel('Press SELECT to start/stop IMAP Glow')
    self.lProgressUpdate = xbmcgui.ControlLabel(320, 560, 1280, 200, '', 'font16', '0xFFFFFFFF')
    self.addControl(self.lProgressUpdate)
    self.lProgressUpdate.setLabel('')

  # Button press
  def onAction(self, action):
    if action == ACTION_SELECT_ITEM:
      try:

        ###########################
        # BULIS PLACE ACTION HERE #
        ###########################

        os.system("sudo python /home/osmc/.kodi/addons/script.imap-glow/resources/lib/imap_glow.py")
#        glow = ImapGlow(12, 16, 18, '/home/osmc/.kodi/addons/script.imap-glow/resources/lib/account_settings.ini')
#        glow = ImapGlow(12, 16, 18, 'special://home/addons/script.imap-glow/resources/lib/account_settings.ini')

        self.lProgressUpdate.setLabel('')
      except:
        self.message("Something wicked happened :(", "Error!")
        sys.exit()

    if (action == ACTION_PREVIOUS_MENU or action == ACTION_NAV_BACK):
      self.close()

  # Display message to user
  def message(self, message, title):
    dialog = xbmcgui.Dialog()
    dialog.ok(title, message)

  # Fetch the current language settings
  def language_settings(self):
    __settings__ = xbmcaddon.Addon(id='script.imap-glow')
    __language__ = __settings__.getLocalizedString
    #self.lExit.setLabel(__language__(10001))
    #self.please_wait_txt = __language__(10010)
    #self.email_success_txt = __language__(10012)
    #self.something_wicked_txt = __language__(10013)

  # Fetch the configuration settings defined by the user
  def get_config_settings(self):
    __settings__ = xbmcaddon.Addon(id='script.imap-glow')
    self.imap_glow_enabled = __settings__.getSetting( "imap_glow_enabled" )
    self.imap_account = __settings__.getSetting( "imap_account" )
    self.imap_username = __settings__.getSetting( "imap_username" )
    self.imap_password = __settings__.getSetting( "imap_password" )
    self.imap_server = __settings__.getSetting( "imap_server" )
    self.imap_port = __settings__.getSetting( "imap_port" )
    self.imap_enable_ssl = __settings__.getSetting( "imap_enable_ssl" )
    self.email_poll_interval = __settings__.getSetting( "email_poll_interval" )
    self.red_email_from = __settings__.getSetting( "red_email_from" )
    self.red_email_subject = __settings__.getSetting( "red_email_subject" )
    self.green_email_from = __settings__.getSetting( "green_email_from" )
    self.green_email_subject = __settings__.getSetting( "green_email_subject" )
    self.blue_email_from = __settings__.getSetting( "blue_email_from" )
    self.blue_email_subject = __settings__.getSetting( "blue_email_subject" )
    self.yellow_email_from = __settings__.getSetting( "yellow_email_from" )
    self.yellow_email_subject = __settings__.getSetting( "yellow_email_subject" )
    self.pink_email_from = __settings__.getSetting( "pink_email_from" )
    self.pink_email_subject = __settings__.getSetting( "pink_email_subject" )
    self.sky_email_from = __settings__.getSetting( "sky_email_from" )
    self.sky_email_subject = __settings__.getSetting( "sky_email_subject" )
    self.white_email_from = __settings__.getSetting( "white_email_from" )
    self.white_email_subject = __settings__.getSetting( "white_email_subject" )

######################
# Start main routine #
######################
if ( __name__ == "__main__" ):
  imap_glow_enabled = 'true'
  imap_account = ''
  imap_username = ''
  imap_password = ''
  imap_server = ''
  imap_port = '993'
  imap_enable_ssl = 'true'
  email_poll_interval = '1'
  red_email_from = ''
  red_email_subject = ''
  green_email_from = ''
  green_email_subject = ''
  blue_email_from = ''
  blue_email_subject = ''
  yellow_email_from = ''
  yellow_email_subject = ''
  pink_email_from = ''
  pink_email_subject = ''
  sky_email_from = ''
  sky_email_subject = ''
  white_email_from = ''
  white_email_subject = ''

  something_wicked_txt = 'Something wicked happened :('
  press_select_txt = 'Press SELECT to begin'

  window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
  if window.getProperty('MyAddonIsRunning') != 'true':
    # Display waiting dialog (like hourglass)
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    mydisplay = ImapGlowAddon()
    mydisplay.language_settings()
    mydisplay.get_config_settings()
    # Remove waiting dialog (like hourglass)
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    mydisplay.doModal()
    del mydisplay
    window.setProperty('MyAddonIsRunning', 'false')

