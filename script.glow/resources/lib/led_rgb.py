#!/usr/bin/env python
# Written By: Phantom Raspberry Blower
# Date: 27-05-2016
# Operate an RGB LED. Supply the pin numbers for 
# red, green & blue leds and choose from seven
# colours: red, green, blue, orange, pink, sky and white

import time
import RPi.GPIO as GPIO

class LedRgb():

  def __init__(self, red_pin, green_pin, blue_pin):
    # Define gpio as BOARD numbering (not BCM naming)
    GPIO.setmode(GPIO.BOARD)
    # Disable warnings caused when you set an LED high that is already high
    GPIO.setwarnings(False)
    # Define the pin numbers for red, green and blue led's
    self.led_pins = (red_pin, green_pin, blue_pin)
    # Setup all the pins as outputs
    for col in self.led_pins:
      GPIO.setup(col, GPIO.OUT)

  def _reset(self):
    # Turn all LED's off
    for col in self.led_pins:
      GPIO.output(col, GPIO.LOW)

  def _colour(self, R, G, B):
    # Turn off all colours
    self._reset()
    self.current_rgb = (R, G, B)
    # Turn on selected colours
    if R == 1: GPIO.output(self.led_pins[0], GPIO.HIGH)
    if G == 1: GPIO.output(self.led_pins[1], GPIO.HIGH)
    if B == 1: GPIO.output(self.led_pins[2], GPIO.HIGH)

  def off(self):
    self._reset()

  def on(self):
    self._colour(self.current_rgb[0],
                 self.current_rgb[1],
                 self.current_rgb[2])

  def red(self):
    self._colour(1,0,0)

  def green(self):
    self._colour(0,1,0)

  def blue(self):
    self._colour(0,0,1)

  def orange(self):
    self._colour(1,1,0)

  def pink(self):
    self._colour(1,0,1)

  def sky(self):
    self._colour(0,1,1)

  def white(self):
    self._colour(1,1,1)

  def flash_led(self, count):
    # Set maximum number of flashes to seven
    if count > 7: count = 7
    # Flash led for each item in count
    while count > 0:
      self.off()
      time.sleep(0.2)
      self.on()
      time.sleep(0.2)
      count -= 1

  def close(self):
    self._reset()
    GPIO.cleanup()

# Check if running stand-alone or imported
if __name__ == '__main__':
  import led_rgb
  try:
    # Prompt user for pin numbers if red, green, blue led's
    led_red_pin = input('Enter the pin number used by the red led: ')
    led_green_pin = input('Enter the pin number used by the green led: ')
    led_blue_pin = input('Enter the pin number used by the blue led: ')
    led_pins = (led_red_pin, led_green_pin, led_blue_pin)
    led = LedRgb(led_red_pin, led_green_pin, led_blue_pin)
    options = {'red' : led.red,
               'green' : led.green,
               'blue' : led.blue,
               'orange' : led.orange,
               'pink' : led.pink,
               'sky' : led.sky,
               'white' : led.white,
               'off' : led.off}
    while True:
      # Prompt user for colour selection
      response = raw_input('Enter a colour (red, green, blue, orange, pink, sky, white or off): ')
      if response in ['exit', 'quit']:
        led.close()
        quit()
      try:
        options[response]()
      except:
        pass
  except KeyboardInterrupt:
    print "\nQuit"

  #Tidy up remaining connections.
  GPIO.cleanup()
