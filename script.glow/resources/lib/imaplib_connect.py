import imaplib
import os
from config_settings import ConfigSettings

def open_connection(verbose=False):
  # Read the config file
  conf = ConfigSettings('account_settings.ini')

  # Connect to the server
  hostname = conf.get_value('server', 'hostname')
  if verbose: print 'Connecting to', hostname
  connection = imaplib.IMAP4_SSL(hostname)

  # Login to our account
  username = conf.get_value('account', 'username')
  password = conf.get_value('account', 'password')
  if verbose: print 'Logging in as', username
  connection.login(username, password)
  return connection

if __name__ == '__main__':
  c = open_connection(verbose=True)
  try:
    print c
  finally:
    c.logout()