#!/usr/bin/env python

# Geocode map image
# Return an image for a given location
# (latitude and longitude)

# Date: 07 March 2016
# Written By: Phantom Raspberry Blower

import Image, urllib, StringIO
from math import log, exp, tan, atan, pi, ceil

EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0

class GeocodeImage():

  # Initialize
  def __init__(self):
    pass

  def latlontopixels(self, lat, lon, zoom):
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = log(tan((90 + lat) * pi/360.0))/(pi/180.0)
    my = (my * ORIGIN_SHIFT) /180.0
    res = INITIAL_RESOLUTION / (2**zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (my + ORIGIN_SHIFT) / res
    return px, py

  def pixelstolatlon(self, px, py, zoom):
    res = INITIAL_RESOLUTION / (2**zoom)
    mx = px * res - ORIGIN_SHIFT
    my = py * res - ORIGIN_SHIFT
    lat = (my / ORIGIN_SHIFT) * 180.0
    lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    lon = (mx / ORIGIN_SHIFT) * 180.0
    return lat, lon

  def geocode_image(self, lat, lon, file_path):
    plat, plon = self.latlontopixels(lat, lon, 17)
    nlat, nlon = self.pixelstolatlon(plat-320, plon+180, 17)
    upperleft = '%f,%f' % (nlat, nlon)
    plat, plon = self.latlontopixels(nlat, nlon, 17)
    nlat, nlon = self.pixelstolatlon(plat+640, plon-360, 17)
    lowerright = '%f,%f' % (nlat, nlon)
    zoom = 18   # be careful not to get too many images!
    map_type = 'hybrid'
    ullat, ullon = map(float, upperleft.split(','))
    lrlat, lrlon = map(float, lowerright.split(','))
    # Set some important parameters
    scale = 1
    maxsize = 640
    # convert all these coordinates to pixels
    ulx, uly = self.latlontopixels(ullat, ullon, zoom)
    lrx, lry = self.latlontopixels(lrlat, lrlon, zoom)
    # calculate total pixel dimensions of final image
    dx, dy = abs(lrx - ulx), abs(uly - lry)
    # calculate rows and columns
    cols, rows = int(ceil(dx/maxsize)), int(ceil(dy/maxsize))
    # calculate pixel dimensions of each small image
    bottom = 120
    length = int(ceil(dx/cols))
    height = int(ceil(dy/rows))
    heightplus = height + bottom
    final = Image.new("RGB", (int(dx), int(dy)))
    for x in range(cols):
        for y in range(rows):
            dxn = length * (0.5 + x)
            dyn = height * (0.5 + y)
            latn, lonn = self.pixelstolatlon(ulx + dxn, uly - dyn - bottom/2, zoom)
            position = ','.join((str(latn), str(lonn)))
            print x, y, position
            urlparams = urllib.urlencode({'center': position,
                                          'zoom': str(zoom),
                                          'size': '%dx%d' % (length, heightplus),
                                          'maptype': map_type,
                                          'sensor': 'false',
                                          'scale': scale})
            url = 'http://maps.google.com/maps/api/staticmap?' + urlparams
            f=urllib.urlopen(url)
            im=Image.open(StringIO.StringIO(f.read()))
            final.paste(im, (int(x*length), int(y*height)))
            final.save(file_path)
    final.show()
    return final

if __name__ == '__main__':
    latitude = input('Enter Latitude:  ')
    longitude = input('Enter Longitude: ')
    gi = GeocodeImage()
    print "Fetching image ..."
    gi.geocode_image(latitude, longitude, '/home/osmc/.kodi/addons/script.imap-glow/resources/lib/image.jpg')
    print "Image saved!"
