#!/usr/bin/env python
# Written By: Phantom Raspberry Blower
# Date: 27-05-2016
# Connect to IMAP server and light an RGB LED
# colours: red, green, blue, orange, pink, sky and white
# Flash the LED to correspond to the number of emails (max. 7)

import time
import datetime
import imaplib_connect
from config_settings import ConfigSettings
from led_rgb import LedRgb

# Class used to break out of nested loop
class BreakIt(Exception): pass

class ImapGlow():

  def __init__(self, red_pin, green_pin, blue_pin, config_settings_path):
    self.led_pins = (red_pin, green_pin, blue_pin)
    self.acct_set_path = config_settings_path
    self.LED = LedRgb(red_pin, green_pin, blue_pin)
    self.email_poll_interval = 60
    self.enable = True
    self.verbose = False

  def date_time_stamp(self):
    # Date and time stamp
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

  def _compile_search_criteria(self, type, config):
    # Compile list of FROM or SUBJECT search criteria
    index = 0
    search_criteria = ''
    for item in config:
      index += 1
      if len(item) > 0:
        if item != ('any' or ''):
          search_criteria = search_criteria + '(%s "'"%s"'") ' % (type, item)
      if index > 1:
        search_criteria = '(OR ' + search_criteria.rstrip() + ') '    
    return search_criteria

  def _fetch_email_count(self, conn, config_setting):
    count = 0
    try:
      conf_set = ConfigSettings(self.acct_set_path)
      from_search_criteria = ''
      subject_search_criteria = ''
      search_criteria = ''
      self.email_poll_interval = int(conf_set.get_value('general', 'email_poll_interval'))
      # Check emails sent from list of senders
      config_from = conf_set.get_value(config_setting, 'from').split('; ')
      config_subject = conf_set.get_value(config_setting, 'subject').split('; ')
      # Compile list of FROM search criteria
      from_search_criteria = self._compile_search_criteria('FROM', config_from)
      # Compile list of FROM search criteria
      subject_search_criteria = self._compile_search_criteria('SUBJECT', config_subject)
      search_criteria = from_search_criteria + subject_search_criteria
      if search_criteria != '':
        # Show only unread emails
        search_criteria = search_criteria + '(UNSEEN)'
        # Search using defined criteria
        typ, msg_ids = conn.search(None, search_criteria)
        # Set email counts
        if msg_ids[0] != '':
          count = len(msg_ids[0].split(' '))
        else:
          count = 0
        if self.verbose == True: print self.date_time_stamp() + ' INBOX has %d email(s) matching %s' % (count, search_criteria)
      else:
        count = 0
    except:
      pass
    return count

  def fetch_email_colour_counts(self):
    try:
      # Open connection to imap server
      c = imaplib_connect.open_connection()
      # Select the email account inbox
      c.select('INBOX', readonly=True)
      # Search each colour category for number of unread emails
      red_emails_count = self._fetch_email_count(c, 'red_senders')
      green_emails_count = self._fetch_email_count(c, 'green_senders')
      blue_emails_count = self._fetch_email_count(c, 'blue_senders')
      orange_emails_count = self._fetch_email_count(c, 'orange_senders')
      pink_emails_count = self._fetch_email_count(c, 'pink_senders')
      sky_emails_count = self._fetch_email_count(c, 'sky_senders')
      white_emails_count = self._fetch_email_count(c, 'white_senders')
      # Close connection to imap server
      c.close()
      c.logout()
    except:
      pass
    return (red_emails_count,
            green_emails_count,
            blue_emails_count,
            orange_emails_count,
            pink_emails_count,
            sky_emails_count,
            white_emails_count)

  def start(self, verbose=False):
    try:
      self.verbose = verbose
      options = {0 : self.LED.red,
                 1 : self.LED.green,
                 2 : self.LED.blue,
                 3 : self.LED.orange,
                 4 : self.LED.pink,
                 5 : self.LED.sky,
                 6 : self.LED.white}
      self.LED.off()
      while self.enable:
        # Fetch emails
        col_counts = self.fetch_email_colour_counts()
        led_duration = 0
        for index in col_counts:
          if index > 0:
            led_duration += 1
        if led_duration > 0:
          led_duration = (self.email_poll_interval / led_duration)
        else:
          time.sleep(email_poll_interval)
        count = 10
        while (count > 0):
          for index in range(0,len(options)):
            if col_counts[index] > 0:
              options[index]()
              self.LED.flash_led(col_counts[index])
              time.sleep(led_duration / 10)
              self.LED.off()
            else:
              self.LED.off()
            if self.enable != True:
              # Break out of nested loop
              raise BreakIt
          count -= 1
    except BreakIt:
      pass
    except:
      self.stop()
    # Tidy up any remaining connections.
    self.LED.close()

  def stop(self):
    self.enable = False

# Check if running stand-alone or imported
if __name__ == '__main__':
  import imap_glow
#  import thread
  try:
    # Prompt user for pin numbers if red, green, blue led's
    led_red_pin = input('Enter the pin number used by the red led: ')
    led_green_pin = input('Enter the pin number used by the green led: ')
    led_blue_pin = input('Enter the pin number used by the blue led: ')
    led_pins = (led_red_pin, led_green_pin, led_blue_pin)
    acct_settings_path = raw_input('Enter the config settings file path: ')
    glow = ImapGlow(led_red_pin, led_green_pin, led_blue_pin, acct_settings_path)
#    thread.start_new_thread(glow.start, (True,))
    glow.start(True)
  except KeyboardInterrupt:
    glow.stop()
    print "\nQuit"
#  finally:
#    glow.stop()  
