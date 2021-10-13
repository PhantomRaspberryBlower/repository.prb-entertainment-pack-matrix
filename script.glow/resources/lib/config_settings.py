import ConfigParser
from encryption import Encryption

class ConfigSettings():

  # Initialize
  def __init__(self, filename):
    self.filename = filename
    self.conf_par = ConfigParser.ConfigParser()

  # Get CPU Serial Number
  def _get_serial(self):
    cpu_serial = '0000000000000000'
    try:
      f = open('/proc/cpuinfo', 'r')
      for line in f:
        if line[0:6] == 'Serial':
          cpu_serial = line[10:26]
      f.close()
    except:
      cpu_serial = 'Error: Unable to get cpu serial number :('
    return cpu_serial

  def get_value(self, section, name):
    self.conf_par.read(self.filename)
    if name == 'password':
      decrypt = Encryption(self._get_serial())
      value = decrypt.decrypt_msg(self.conf_par.get(section, name))
    else:
      value = self.conf_par.get(section, name)
    return value

  def set_value(self, section, name, value):
    if name == 'password':
      encrypt = Encryption(self._get_serial())
      self.conf_par.set(section, name, encrypt.encrypt_msg(value))
    else:
      conf_par.set(section, name, value)
    with open(self.filename, 'wb') as configfile:
      self.conf_par.write(configfile)

