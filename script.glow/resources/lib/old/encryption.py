#!/usr/bin/env python

# Encryption
# A quick way to encrypt and decrypt using AES
# and displays results in base 64

# Date: 07 March 2016
# Written By: Phantom Raspberry Blower

import base64
from Crypto.Cipher import AES

class Encryption():

  # Initialize
  def __init__(self, key):
    # Pad with leading zeros to ensure key length = 16
    self.key = key.zfill(16)
    self.iv = 'PRB StrikesAgain'

  # Encrypt message
  def encrypt_msg(self, msg):
    objAES = AES.new(self.key, AES.MODE_CFB, self.iv)
    cipher_txt = objAES.encrypt(msg)
    return base64.b64encode(cipher_txt)

  # Decrypt message
  def decrypt_msg(self, msg):
    objAES = AES.new(self.key, AES.MODE_CFB, self.iv)
    cipher_txt = base64.b64decode(msg)
    return objAES.decrypt(cipher_txt)