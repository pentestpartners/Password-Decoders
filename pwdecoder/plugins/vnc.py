#!/usr/bin/python

# Used VNC mangled DES, stolen from https://github.com/trinitronx/vncpasswd.py
import vncd3des as des
import binascii

class wyse(object):

 def init(self):
  conf={
   'name':'vnc',
   'author':'tautology',
   'hashes':[
    {
     'name': 'vnc',
     'decode': self.vncdecode,
    }
   ]
  }
  return conf

 def vncdecode(self,data,options):
  key=binascii.unhexlify('17526b06234e5807')
  pw=binascii.unhexlify(data)

  cipher=des.deskey(key, True)
  return des.desfunc(pw,cipher)
