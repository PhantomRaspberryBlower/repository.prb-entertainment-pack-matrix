#!/usr/bin/env python

# Moondial
# At sunset the red led will light and change colours
# throughout the day until blue representing sunrise

# Date: 07 March 2016
# Written By: Phantom Raspberry Blower

from sunrise import Sun
import datetime as dt

import math

sunrise = ''
sunset = ''
night_duration = ''
daylight_duration = ''
current_time = ''
col_interval = ''
current_colour = ''
latitude = ''
longitude = ''

class Moondial():

  # Initialize
  def __init__(self):
    self.current_time = dt.datetime.now()
    self.current_time = self.current_time.replace(microsecond=0)

  def get_current_colour(self,lat=52.68,long=-1.187): # default Anstey, Leicester, UK):
    self.latitude = lat
    self.longitude = long
    led_colours = ["Off", "Red", "Yellow", "Green", "Blue", "Sky", "Pink", "White"]
    self.sunrise = dt.datetime.combine(dt.datetime.now(), Sun(lat, long).sunrise())

    if self.current_time < self.sunrise:
      yesterday = (dt.datetime.now() - dt.timedelta(days=1))
      yesterday = yesterday.replace(microsecond=0)
      self.sunset = dt.datetime.combine(yesterday, Sun(lat, long).sunset(yesterday))
    else:
      self.sunset = dt.datetime.combine(dt.datetime.now(), Sun(lat, long).sunset())
      if self.current_time > self.sunset:
        tomorrow = (dt.datetime.now() + dt.timedelta(days=1))
        self.sunrise = dt.datetime.combine(tomorrow, Sun(lat, long).sunrise(tomorrow))

    if self.current_time < self.sunrise and self.current_time > self.sunset:
      print "Between sunset and sunrise"
      self.night_duration = self.sunrise - self.sunset
      self.daylight_duration = dt.timedelta(days=1) - self.night_duration
    else:
      print "Between sunrise and sunset"
      self.night_duration = self.sunrise - self.sunset
      self.daylight_duration = dt.timedelta(days=1) - self.night_duration

    self.col_interval = self.night_duration / 6
    self.current_colour = (self.current_time - self.sunset)
    self.current_colour = (self.current_colour.seconds / self.col_interval.seconds) + 1

    self.current_colour = int(math.ceil(self.current_colour))

    if self.current_colour > 6:
      self.current_colour = 0

    print "Colour Number:", self.current_colour
    print "Latitude:", self.latitude
    print "Longitude:", self.longitude

    self.current_colour = led_colours[self.current_colour]
    print "Current Time:", self.current_time
    print "Sunrise:", self.sunrise
    print "Sunset:", self.sunset
    print "Night_Duration:", self.night_duration
    print "Daylight Duration:", self.daylight_duration
    print "Colour Interval:", self.col_interval
    print "Current Colour:", self.current_colour
    dict = {"Current Time" : self.current_time, 
            "Sunrise" : self.sunrise,
            "Sunset" : self.sunset,
            "Duration" : self.night_duration,
            "Colour Interval" : self.col_interval,
            "Current Colour" : self.current_colour}
    return dict

if __name__ == '__main__':
    md = Moondial()
    md.get_current_colour(52.68,-1.187)