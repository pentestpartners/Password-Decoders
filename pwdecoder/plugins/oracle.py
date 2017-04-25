#!/usr/bin/python

import binascii
import base64
from Crypto.Cipher import DES

unpad = lambda s : s[0:-ord(s[-1])]

class oracle(object):

 def init(self):
  conf={
   'name':'oracle',
   'author':'tautology',
   'hashes':[
    {
     'name': 'dblink11',
     'decode': self.dblink11,
    }
   ]
  }
  return conf

 def dblink11(self, data, options):
  key=binascii.unhexlify(data[2:18])
  pw=binascii.unhexlify(data[18:])

  cipher=DES.new(key, DES.MODE_CBC, '\0' * 8)
  return unpad(cipher.decrypt(pw))

