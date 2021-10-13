#!/usr/bin/env python

# Moondial
# At sunset the led will light up and change colours throughout the
# night until sunrise. The colour sequence is red, yellow, green, sky,
# blue, pink; with red illuminating immediately after sunset and pink
# switches off just before sunrise.

# Date: 07 March 2016
# Written By: Phantom Raspberry Blower

import math					# Calculate ceiling of colour change interval
import datetime as dt			# Manipulate dates and times
from timezone import LocalTimezone	# Adjust times based on local timezone

from sunrise import Sun			# Calculate sunrise and sunset times


sunrise = ''				# Sunrise time
sunset = ''					# Sunset time
current_solar_status = ''           # Current status of daylight or night-time
night_duration = ''			# Duration between sunset and sunrise
daylight_duration = ''			# Duration between sunrise and sunset
current_time = ''				# Current time
col_interval = ''				# Duration of colour change interval
current_colour_number = 0		# Current colour item number
current_colour = ''			# Current colour name
latitude = ''				# Latitude as decimal value
longitude = ''				# Longitude as deciaml value

class Moondial():

  # Initialize
  def __init__(self):
    # Set the current time adjusting for local timezone and strip out microsends
    self.current_time = dt.datetime.now(tz=LocalTimezone())
    self.current_time = self.current_time.replace(microsecond=0)

  def get_current_colour(self,lat=52.68,long=-1.187): # default Anstey, Leicester, UK
    # Set the latitude and longitude co-ordinates
    self.latitude = lat
    self.longitude = long

    # Define the led colours
    led_colours = ["Off", "Red", "Yellow", "Green", "Blue", "Sky", "Pink", "White"]

    # Set the sunrise time adjusting for local timezone and strip out microsends
    self.sunrise = dt.datetime.combine(self.current_time, Sun(lat, long).sunrise(self.current_time))
    self.sunrise = self.sunrise.replace(microsecond=0)

    # Set the sunset time adjusting for local timezone and strip out microsends
    self.sunset = dt.datetime.combine(self.current_time, Sun(lat, long).sunset(self.current_time))
    self.sunset = self.sunset.replace(microsecond=0)

    # Convert a timezone-aware datetime object to local timezone and strip out microseconds
    self.current_time = dt.datetime.combine(self.current_time, dt.datetime.now(tz=LocalTimezone()).time())
    self.current_time = self.current_time.replace(microsecond=0)

    if self.current_time > self.sunrise and self.current_time < self.sunset:
      # Day time
      self.current_solar_status = 'Between sunrise and sunset'
      self.daylight_duration = self.sunset - self.sunrise
      self.night_duration = dt.timedelta(days=1) - self.daylight_duration
    else:
      # Night time
      self.current_solar_status = 'Between sunset and sunrise'
      if self.current_time < self.sunrise:
	  # Calculate yesterdays sunset time
        yesterday = (dt.datetime.now(tz=LocalTimezone()) - dt.timedelta(days=1))
        yesterday = yesterday.replace(microsecond=0)
        self.sunset = dt.datetime.combine(yesterday, Sun(lat, long).sunset(yesterday))
      else:
	  # Calculate tomorrows sunrise time
        tomorrow = (dt.datetime.now(tz=LocalTimezone()) + dt.timedelta(days=1))
        tomorrow = tomorrow.replace(microsecond=0)
        self.sunrise = dt.datetime.combine(tomorrow, Sun(lat, long).sunrise(tomorrow))

      # Calculate daylight and night-time duration
      self.night_duration = self.sunrise - self.sunset
      self.daylight_duration = dt.timedelta(days=1) - self.night_duration

    # Calculate the colour change interval
    self.col_interval = self.night_duration / 6

    # Calculate the current colour item number
    self.current_colour_number = (self.current_time - self.sunset)
    self.current_colour_number = (self.current_colour_number.seconds / self.col_interval.seconds) + 1
    self.current_colour_number = int(math.ceil(self.current_colour_number))

    # Check if current colour item number is out of bounds
    if self.current_colour_number > 6:
      self.current_colour_number = 0

    # Get current colour description
    self.current_colour = led_colours[self.current_colour_number]

    # Display the results
    print self.current_solar_status
    print "Colour Number:", self.current_colour_number
    print "Latitude:", self.latitude
    print "Longitude:", self.longitude
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