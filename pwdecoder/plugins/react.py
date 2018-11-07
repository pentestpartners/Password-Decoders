#!/usr/bin/python

# Needs Cryptodome as it supports AES.MODE_GCM
import base64
from Cryptodome.Cipher import AES

class react(object):

 def init(self):
  conf={
   'name':'react',
   'author':'tautology',
   'hashes':[
    {
     'name': 'keychain',
     'decode': self.keychaindecode,
     'options': [ 'key' ]
    }
   ]
  }
  return conf

 def keychaindecode(self, data, options):
  if not options['key']:
   print("No key provided")
   exit(1)
 
  key=base64.b64decode(options['key'])
  iv=base64.b64decode(data)[2:14]
  pw=base64.b64decode(data)[14:]

  cipher=AES.new(key, AES.MODE_GCM, iv)
  out=cipher.decrypt(pw)

  # remove tag (16 bytes)
  return out[:len(out)-16]
