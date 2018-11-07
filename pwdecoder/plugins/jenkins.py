#!/usr/bin/python

import base64
import struct
from hashlib import sha256
from Crypto.Cipher import AES

unpad = lambda s : s[0:-ord(s[-1])]

class jenkins(object):

 def init(self):
  conf={
   'name':'jenkins',
   'author':'tautology',
   'hashes':[
    {
     'name': 'jenkins',
     'decode': self.jenkinsdecode,
     'options': [ 'master', 'secret' ]
    }
   ]
  }
  return conf

 def jenkinsdecode(self, data, options):
  if not options['master']:
   print("No master key file provided")
   exit(1)
  try:
   master=open(options['master'], "rb").read()
  except:
   print("Could not open " + options['master'])
   exit(1)
  masterkey=sha256(master).digest()[:16]

  if not options['secret']:
   print("No secrets key file provided")
   exit(1)
  try:
   secret=open(options['secret'], "rb").read()
  except:
   print("Could not open " + options['secret'])
   exit(1)
 
  # decrypt secret key
  cipher=AES.new(masterkey, AES.MODE_ECB)
  secretkey=cipher.decrypt(secret)[:16]

  cooked=base64.b64decode(data)
  if cooked[0] != '\x01':
   print("This does not appear to be a valid hash")
   exit(1)

  ivlen=struct.unpack('>i', cooked[1:5])[0]
  if ivlen % 16 != 0:
   print("iv length needs to be a multiple of 16")
   exit(1)
  dlen=struct.unpack('>i', cooked[5:9])[0]
  if dlen % 16 != 0:
   print("Data length needs to be a multiple of 16")
   exit(1)
  
  istart=9
  iend=9+ivlen
  dstart=iend
  dend=dstart+dlen
  iv=cooked[istart:iend]
  crypted=cooked[dstart:dend]

  cipher=AES.new(secretkey, AES.MODE_CBC, iv)
  out=cipher.decrypt(crypted)

  # remove padding
  return unpad(out)
