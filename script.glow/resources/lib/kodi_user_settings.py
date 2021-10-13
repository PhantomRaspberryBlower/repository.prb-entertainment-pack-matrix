#!/usr/bin/env python

# Used to fetch user defined settings in kodi
import xml.etree.ElementTree as et

from config_settings import ConfigSettings

class KodiUserSettings:

  # Initilize Object
  def __init__(self, path):
    self.output_path = path

  # Fetch user settings (set via the kodi addon: script.snapshot)
  def get_kodi_user_settings(self, path):
    email_notifications = 'false'
    imap_server = ''
    email_poll_interval = ''
    account_username = ''
    account_password = ''
    red_senders_from = ''
    red_senders_subject = ''
    green_senders_from = ''
    green_senders_subject = ''
    blue_senders_from = ''
    blue_senders_subject = ''
    orange_senders_from = ''
    orange_senders_subject = ''
    pink_senders_from = ''
    pink_senders_subject = ''
    sky_senders_from = ''
    sky_senders_subject = ''
    white_senders_from = ''
    white_senders_subject = ''

    # Open the settings xml file (.kodi/userdata/addon_data/script.snapshot)
    tree = et.parse(path)
    root = tree.getroot()
    for child in root:
      if child.get('id') == 'email_notifications':
        email_notifications = child.get('value')
      elif child.get('id') == 'imap_server':
        imap_server = child.get('value')
      elif child.get('id') == 'email_poll_interval':
        email_poll_interval = child.get('value')
      elif child.get('id') == 'account_username':
        account_username = child.get('value')
      elif child.get('id') == 'account_password':
        account_password = child.get('value')
      elif child.get('id') == 'red_senders_from':
        red_senders_from = child.get('value')
      elif child.get('id') == 'red_senders_subject':
        red_senders_subject = child.get('value')
      elif child.get('id') == 'green_senders_from':
        green_senders_from = child.get('value')
      elif child.get('id') == 'green_senders_subject':
        green_senders_subject = child.get('value')
      elif child.get('id') == 'blue_senders_from':
        blue_senders_from = child.get('value')
      elif child.get('id') == 'blue_senders_subject':
        blue_senders_subject = child.get('value')
      elif child.get('id') == 'orange_senders_from':
        orange_senders_from = child.get('value')
      elif child.get('id') == 'orange_senders_subject':
        orange_senders_subject = child.get('value')
      elif child.get('id') == 'pink_senders_from':
        pink_senders_from = child.get('value')
      elif child.get('id') == 'pink_senders_subject':
        pink_senders_subject = child.get('value')
      elif child.get('id') == 'sky_senders_from':
        sky_senders_from = child.get('value')
      elif child.get('id') == 'sky_senders_subject':
        sky_senders_subject = child.get('value')
      elif child.get('id') == 'white_senders_from':
        white_senders_from = child.get('value')
      elif child.get('id') == 'white_senders_subject':
        white_senders_subject = child.get('value')

    tup = (email_notifications, imap_server, email_poll_interval, account_username, account_password,
           red_senders_from, red_senders_subject, green_senders_from, green_senders_subject,
           blue_senders_from, blue_senders_subject, orange_senders_from, orange_senders_subject,
           pink_senders_from, pink_senders_subject, sky_senders_from, sky_senders_subject,
           white_senders_from, white_senders_subject)
    return tup

  def update_kodi_user_settings(self, kodi_path, settings_path):
    kodi_settings_tup = get_kodi_user_settings(kodi_path)
    conf_set = ConfigSettings(settings_path)
    conf_set.set_value('general', 'email_notifications', kodi_settings_tup[0])
    conf_set.set_value('server', 'hostname', kodi_settings_tup[1])
    conf_set.set_value('general', 'email_poll_interval', kodi_settings_tup[2])
    conf_set.set_value('account', 'username', kodi_settings_tup[3])
    conf_set.set_value('account', 'password', kodi_settings_tup[4])
    conf_set.set_value('red_senders', 'from', kodi_settings_tup[5])
    conf_set.set_value('red_senders', 'subject', kodi_settings_tup[6])
    conf_set.set_value('green_senders', 'from', kodi_settings_tup[7])
    conf_set.set_value('green_senders', 'subject', kodi_settings_tup[8])
    conf_set.set_value('blue_senders', 'from', kodi_settings_tup[9])
    conf_set.set_value('blue_senders', 'subject', kodi_settings_tup[10])
    conf_set.set_value('orange_senders', 'from', kodi_settings_tup[11])
    conf_set.set_value('orange_senders', 'subject', kodi_settings_tup[12])
    conf_set.set_value('pink_senders', 'from', kodi_settings_tup[13])
    conf_set.set_value('pink_senders', 'subject', kodi_settings_tup[14])
    conf_set.set_value('sky_senders', 'from', kodi_settings_tup[15])
    conf_set.set_value('sky_senders', 'subject', kodi_settings_tup[16])
    conf_set.set_value('white_senders', 'from', kodi_settings_tup[17])
    conf_set.set_value('white_senders', 'subject', kodi_settings_tup[18])
