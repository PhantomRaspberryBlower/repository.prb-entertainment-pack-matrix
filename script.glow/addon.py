#!/bin/python

# Application used to control IMAP Glow candle by
# sending UDP multicast packets over the network
# and displays a response.
# Written by: Phantom Raspberry Blower
# Date:       01-07-2016

import xbmc, xbmcgui
import time

import threading # Bulis - Possibly remove!!!
from resources.lib.imap_glow import ImapGlow
 
# Keymap of remote control buttons
ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10 
ACTION_NAV_BACK = 92
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_HIGHLIGHT_ITEM = 8
ACTION_SHOW_INFO = 11
ALIGN_CENTER = 6

# UDP socket settings
BUFFER_SIZE = 1024
UDP_BROADCAST_IP = '224.1.1.1'
UDP_PORT = 4569

MODES = ['Off', 'Temperature', 'Sundial', 'Security', 'Night Light', 'Morse Code', 'Moondial', 'Email']
COLOURS = ['Off', 'Red', 'Green', 'Blue', 'Yellow', 'Pink', 'Sky', 'White']

IMG_PATH = 'special://home/addons/script.glow/resources/images/'
COMMANDS_PATH = 'special://home/addons/script.glow/resources/lib/commands.py'

current_mode = 'Off'
current_colour = 'Off'
respond_button = False
email_started = False
moondial_started = False
sundial_started = False

class MyGlow(xbmcgui.Window):
  def __init__(self):
    # Set Background Image
    self.addControl(xbmcgui.ControlImage(0, 0, 1280, 720, 'special://home/addons/script.glow/Background.png'))
    # Add Mode list
    self.lstMode = xbmcgui.ControlList(30, 40, 300, 75, font='font16', textColor='0xFF2E2F31', selectedColor='0xFF00FFFF', _space=10)
    self.addControl(self.lstMode)
    self.lstMode.addItems(MODES)
    self.lstMode.selectItem(0)
    self.respond_button = False
    self.email_started = False
    self.moondial_started = False
    self.sundial_started = False

    # Set Rotary Knob Image
    self.imgRotaryKnob = xbmcgui.ControlImage(43, 125, 410, 416, IMG_PATH+'PRB_Knob_Off.png')
    self.addControl(self.imgRotaryKnob)

    # Set Colour Button Images
    self.imgRedButton = xbmcgui.ControlImage(184, 583, 139, 55, IMG_PATH+'PRB_Red_Button_On.png')
    self.addControl(self.imgRedButton)
    self.imgRedButton.setVisible(False)
    self.imgGreenButton = xbmcgui.ControlImage(339, 583, 139, 55, IMG_PATH+'PRB_Green_Button_On.png')
    self.addControl(self.imgGreenButton)
    self.imgGreenButton.setVisible(False)
    self.imgBlueButton = xbmcgui.ControlImage(493, 583, 139, 55, IMG_PATH+'PRB_Blue_Button_On.png')
    self.addControl(self.imgBlueButton)
    self.imgBlueButton.setVisible(False)
    self.imgYellowButton = xbmcgui.ControlImage(648, 583, 139, 55, IMG_PATH+'PRB_Yellow_Button_On.png')
    self.addControl(self.imgYellowButton)
    self.imgYellowButton.setVisible(False)
    self.imgPinkButton = xbmcgui.ControlImage(802, 583, 139, 55, IMG_PATH+'PRB_Pink_Button_On.png')
    self.addControl(self.imgPinkButton)
    self.imgPinkButton.setVisible(False)
    self.imgSkyButton = xbmcgui.ControlImage(957, 583, 139, 55, IMG_PATH+'PRB_Sky_Button_On.png')
    self.addControl(self.imgSkyButton)
    self.imgSkyButton.setVisible(False)
    self.imgWhiteButton = xbmcgui.ControlImage(1111, 583, 139, 55, IMG_PATH+'PRB_White_Button_On.png')
    self.addControl(self.imgWhiteButton)
    self.imgWhiteButton.setVisible(False)

    # Add night light buttons
    self.butOff = xbmcgui.ControlButton(31, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butOff)
    self.butOff.setVisible(False)
    self.butRed = xbmcgui.ControlButton(184, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butRed)
    self.butRed.setVisible(False)
    self.butGreen = xbmcgui.ControlButton(339, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butGreen)
    self.butGreen.setVisible(False)
    self.butBlue = xbmcgui.ControlButton(493, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butBlue)
    self.butBlue.setVisible(False)
    self.butYellow = xbmcgui.ControlButton(648, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butYellow)
    self.butYellow.setVisible(False)
    self.butPink = xbmcgui.ControlButton(802, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butPink)
    self.butPink.setVisible(False)
    self.butSky = xbmcgui.ControlButton(957, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butSky)
    self.butSky.setVisible(False)
    self.butWhite = xbmcgui.ControlButton(1111, 583, 139, 55, '', alignment=ALIGN_CENTER, font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butWhite)
    self.butWhite.setVisible(False)

    # Add morse code controls
    self.butMorseCode = xbmcgui.ControlButton(545, 170, 612, 50, 'Select to enter text', font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    self.addControl(self.butMorseCode)
    self.butMorseCode.setVisible(False)

    self.setFocus(self.lstMode)

    # Set button navigation
    self.butRed.controlUp(self.lstMode)
    self.butRed.controlRight(self.butGreen)
    self.butRed.controlLeft(self.butOff)
    self.butGreen.controlUp(self.lstMode)
    self.butGreen.controlRight(self.butBlue)
    self.butGreen.controlLeft(self.butRed)
    self.butBlue.controlUp(self.lstMode)
    self.butBlue.controlRight(self.butYellow)
    self.butBlue.controlLeft(self.butGreen)
    self.butYellow.controlUp(self.lstMode)
    self.butYellow.controlRight(self.butPink)
    self.butYellow.controlLeft(self.butBlue)
    self.butPink.controlUp(self.lstMode)
    self.butPink.controlRight(self.butSky)
    self.butPink.controlLeft(self.butYellow)
    self.butSky.controlUp(self.lstMode)
    self.butSky.controlRight(self.butWhite)
    self.butSky.controlLeft(self.butPink)
    self.butWhite.controlUp(self.lstMode)
    self.butWhite.controlLeft(self.butSky)
    self.butWhite.controlRight(self.butOff)
    self.butOff.controlUp(self.lstMode)
    self.butOff.controlLeft(self.butWhite)
    self.butOff.controlRight(self.butRed)
    self.butMorseCode.controlUp(self.lstMode)
    self.butMorseCode.controlLeft(self.lstMode)

  def msg_response(self):
    udp_msg = ImapGlow()
    local_ip = udp_msg.get_ip()
    local_ip = '192.168.0.30'
    start_clk = time.time()
    try:
      # Wait upto 6 seconds for a reply from network devices
      while (time.time() - start_clk) < 6:
        data, sender = udp_msg.recv()
        if sender != local_ip:
          self.msg_notification(data, sender, xbmcgui.NOTIFICATION_INFO, 2000)
          return data, sender
      if (time.time() - start_clk) > 5:
        self.msg_notification('No response from Glow', local_ip, xbmcgui.NOTIFICATION_WARNING, 3000)
        return 'Glow did not respond', local_ip
    except:
      if (time.time() - start_clk) > 5:
        self.msg_notification('No response from Glow', local_ip, xbmcgui.NOTIFICATION_WARNING, 3000)
        return 'Glow did not respond', local_ip

  def onAction(self, action):
    # Response to remote control button presses
    if (action == ACTION_PREVIOUS_MENU or action == ACTION_NAV_BACK):
      self.close()
    if action == ACTION_MOVE_UP:
      if self.respond_button == False:
        self.onControl(self.lstMode)
      else:
        self.onControl(self.lstMode)
        self.respond_button = False
        self.setFocus(self.lstMode)
    if action == ACTION_MOVE_DOWN:
      if self.respond_button == False:
        self.onControl(self.lstMode)
      else:
        self.onControl(self.lstMode)
        self.respond_button = False
        self.setFocus(self.lstMode)
    if action == ACTION_SELECT_ITEM:
      lstItem = self.lstMode.getSelectedItem()
      if lstItem.getLabel() == 'Email':
        self.email_started = not self.email_started
        if self.email_started == True:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_1_Red.png')
          self._imap_light('imap_start')
        else:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_1.png')
          self._imap_light('imap_stop')
      if lstItem.getLabel() == 'Off':
        self._imap_light('poweroff') 
      if lstItem.getLabel() == 'Moondial':
        self.moondial_started = not self.moondial_started
        if self.moondial_started == True:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_2_Red.png')
          self._moondial('moondial_start')
        else:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_2.png')
          self._moondial('moondial_stop')
      if lstItem.getLabel() == 'Sundial':
        self.sundial_started = not self.sundial_started
        if self.sundial_started == True:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_6_Red.png')
          #self._sundial('sundial_start')
        else:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_6.png')
          #self._sundial('sundial_stop')
      self.msg_response()

  def onFocus(self, controlId):
#    if controlId == self.lstMode.getFocusId()
    self.message('', 'Got Focus')

  def onControl(self, control):
    lstItem = self.lstMode.getSelectedItem()
   # Respond to selected button
    if control == self.lstMode:
      self.butRed.setVisible(False)
      self.imgRedButton.setVisible(False)
      self.butGreen.setVisible(False)
      self.butBlue.setVisible(False)
      self.butYellow.setVisible(False)
      self.butPink.setVisible(False)
      self.butSky.setVisible(False)
      self.butWhite.setVisible(False)
      self.butOff.setVisible(False)
      self.butMorseCode.setVisible(False)
      if lstItem.getLabel() == 'Off':
        self.current_mode = 'Off'
        self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_Off.png')
      if lstItem.getLabel() == 'Email':
        self.current_mode = 'Email'
        if self.email_started == True:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_1_Red.png')
        else:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_1.png')         
      elif lstItem.getLabel() == 'Moondial':
        self.current_mode = 'Moondial'
        if self.moondial_started == True:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_2_Red.png')
        else:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_2.png')         
      elif lstItem.getLabel() == 'Morse Code':
        self.respond_button = True
        self.current_mode = 'Morse Code'
        self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_3.png')
        self.butMorseCode.setVisible(True)
        self.setFocus(self.butMorseCode)
      elif lstItem.getLabel() == 'Night Light':
        self.respond_button = True
        self.current_mode = 'Night Light'
        self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_4.png')
        self.butRed.setVisible(True)
        self.butGreen.setVisible(True)
        self.butBlue.setVisible(True)
        self.butYellow.setVisible(True)
        self.butPink.setVisible(True)
        self.butSky.setVisible(True)
        self.butWhite.setVisible(True)
        self.butOff.setVisible(True)
        self.setFocus(self.butRed)
      elif lstItem.getLabel() == 'Security':
        self.current_mode = 'Security'
        self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_5.png')
      elif lstItem.getLabel() == 'Sundial':
        self.current_mode = 'Sundial'
        if self.sundial_started == True:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_6_Red.png')
        else:
          self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_6.png')
      elif lstItem.getLabel() == 'Temperature':
        self.current_mode = 'Temperature'
        self.imgRotaryKnob.setImage(IMG_PATH+'PRB_Knob_7.png')
      return None
    if lstItem.getLabel() == 'Email':
      pass
    if lstItem.getLabel() == 'Night Light':
      if control == self.butOff:
        self.current_colour = 'Off'
      elif control == self.butRed:
        self.current_colour = 'Red'
      elif control == self.butGreen:
        self.current_colour = 'Green'
      elif control == self.butBlue:
        self.current_colour = 'Blue'
      elif control == self.butYellow:
        self.current_colour = 'Yellow'
      elif control == self.butPink:
        self.current_colour = 'Pink'
      elif control == self.butSky:
        self.current_colour = 'Sky'
      elif control == self.butWhite:
        self.current_colour = 'White'
      colour = self.current_colour.lower()
      self._colour_button(colour)
      self._night_light(colour)
    if lstItem.getLabel() == 'Morse Code':
      if control == self.butMorseCode:
        self._morse_code_light(control)
    # Wait for response from network devices
    #self.msg_response()

  def _imap_light(self, command):
    # Send imap light request
    xbmc.executebuiltin('XBMC.RunScript('+COMMANDS_PATH+', -m %s)' % command, True)

  def _colour_button(self, colour):
    self.imgRedButton.setVisible(False)
    self.imgGreenButton.setVisible(False)
    self.imgBlueButton.setVisible(False)
    self.imgYellowButton.setVisible(False)
    self.imgPinkButton.setVisible(False)
    self.imgSkyButton.setVisible(False)
    self.imgWhiteButton.setVisible(False)
    if colour == 'red':
      self.imgRedButton.setVisible(True)
    elif colour == 'green':
      self.imgGreenButton.setVisible(True)
    elif colour == 'blue':
      self.imgBlueButton.setVisible(True)
    elif colour == 'yellow':
      self.imgYellowButton.setVisible(True)
    elif colour == 'pink':
      self.imgPinkButton.setVisible(True)
    elif colour == 'sky':
      self.imgSkyButton.setVisible(True)
    elif colour == 'white':
      self.imgWhiteButton.setVisible(True)

  def _night_light(self, colour):
    # Send night light colour request
    xbmc.executebuiltin('XBMC.RunScript('+COMMANDS_PATH+', -m nightlight_%s)' % colour, True)

  def _morse_code_light(self, control):
    default_text = str(control.getLabel()).upper()
    if default_text == 'SELECT TO ENTER TEXT':
      default_text = ''
    dialog = xbmcgui.Dialog()
    morse_text = dialog.input('Enter text to convert to Morse Code', default_text, type=xbmcgui.INPUT_ALPHANUM)
    control.setLabel(morse_text.upper(), font='font16', textColor='0xFFFFFFFF', focusedColor='0xFF00FFFF')
    # Send morse code request
    xbmc.executebuiltin('XBMC.RunScript('+COMMANDS_PATH+', -m morsecode_%s)' % morse_text, True)

  def _moondial(self, command):
    # Send moondial request
    xbmc.executebuiltin('XBMC.RunScript('+COMMANDS_PATH+', -m %s)' % command, True)

  def _sundial(self, command):
    # Send sundial request
    xbmc.executebuiltin('XBMC.RunScript('+COMMANDS_PATH+', -m %s)' % command, True)

  def msg_notification(self, heading, message, icon, duration):
    # Show message notification
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, message, icon, duration)

  def message(self, heading, message):
    # Show message until user responds
    dialog = xbmcgui.Dialog()
    dialog.ok(heading, message)

window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
if window.getProperty('MyAddonIsRunning') != 'true':
  mydisplay = MyGlow()
  # Remove waiting dialog (like hourglass)
  xbmc.executebuiltin("Dialog.Close(busydialog)")
  mydisplay .doModal()
  del mydisplay
  window.setProperty('MyAddonIsRunning', 'false')
