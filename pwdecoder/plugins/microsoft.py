#!/usr/bin/python

import binascii
import base64
from Crypto.Cipher import AES

unpad = lambda s : s[0:-ord(s[-1])]

class microsoft(object):

 def pad(self, target):
  return target + ('=' * ((4 - len(target) % 4) % 4))

 def init(self):
  conf={
   'name':'microsoft',
   'author':'tautology',
   'hashes':[
    {
     'name': 'cpassword',
     'decode': self.cpassworddecode,
    }
   ]
  }
  return conf

 def cpassworddecode(self, data, options):
  key=binascii.unhexlify('4e9906e8fcb66cc9faf49310620ffee8f496e806cc057990209b09a433b66c1b')
  pw=base64.b64decode(self.pad(data))

  cipher=AES.new(key, AES.MODE_CBC, '\0' * 16)
  return unpad(cipher.decrypt(pw))

