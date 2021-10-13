#!/usr/bin/env python

# Geocode
# Return the address and location for a given postcode

# Date: 07 March 2016
# Written By: Phantom Raspberry Blower

import requests				# Used to request web pages
import Image, urllib, StringIO

class Geocode():

  # Initialize
  def __init__(self):
    self.addr = ''

  def geocode_postcode(self, postcode):
    self.geocode(postcode)

  def _clear(self):
    self.post_code = ''
    self.addr = ''
    self.addr_label = ''
    self.formatted_addr = ''
    self.lat = 0.0
    self.lon = 0.0

  def geocode(self, postcode):
    self._clear()
    self.post_code = postcode.upper()
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': postcode}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    self.lat = location['lat']
    self.lon = location['lng']
    address_components = results[0]['address_components']
    for item in range(1, len(address_components)):
      if item > 1:
        self.addr = "%s\n" % self.addr
      self.addr = "%s%s" % (self.addr, address_components[item]['long_name'])
    self.formatted_addr = results[0]['formatted_address']

  def image(self):    
    position = '%s, %s' % (str(self.lat), str(self.lon))
    zoom = 17
    scale = 1
    final = Image.new("RGB", (640, 360))
    urlparams = urllib.urlencode({'center': position,
                                  'zoom': str(zoom),
                                  'size': '%dx%d' % (640, 360),
                                  'maptype': 'street',
                                  'sensor': 'false',
                                  'scale': scale})
    url = 'http://maps.google.com/maps/api/staticmap?' + urlparams
    f=urllib.urlopen(url)
    im=Image.open(StringIO.StringIO(f.read()))
    final.paste(im)
    final.save('/home/osmc/.kodi/addons/script.imap-glow/resources/lib/image.jpg')
    return im

  def postcode(self):
    return self.post_code

  def location(self):
    return [self.latitude(), self.longitude()]

  def latitude(self):
    return self.lat

  def longitude(self):
    return self.lon

  def address(self):
    return self.addr

  def address_label(self):
    return str(self.formatted_address()).replace(", ", ",\n")

  def formatted_address(self):
    return str(self.formatted_addr)

if __name__ == '__main__':
    postcode = raw_input('Enter Postcode: ').upper()
    gc = Geocode()
    gc.geocode_postcode(postcode)
    print "\nAddress:"
    print "         ", gc.address_label().replace("\n", "\n          ")
    print "\nLocation:"
    print "          Latitude:  ", gc.latitude()
    print "          Longitude: ", gc.longitude()
    print "\nSingle-line Address:"
    print "         ", gc.formatted_address(), "\n"
    gc.image()
