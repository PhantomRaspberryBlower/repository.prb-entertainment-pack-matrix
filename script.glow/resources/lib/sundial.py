#!/usr/bin/env python

# Sundial
# At sunrise the red led will light and change colours
# throughout the day until blue representing sunset

# Date: 07 March 2016
# Written By: Phantom Raspberry Blower

from sunrise import Sun

class Sundial():

  # Initialize
  def __init__(self):
    # Pad with leading zeros to ensure key length = 16
    print('Sunrise: %s' % Sun().sunrise())
    print('Sunset: %s' % Sun().sunset())
