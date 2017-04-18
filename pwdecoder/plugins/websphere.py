#!/usr/bin/python

import base64

class websphere(object):

 def init(self):
  conf={
   'name':'websphere',
   'author':'tautology',
   'hashes':[
    {
     'name': 'websphere',
     'decode': self.webspheredecode,
    }
   ]
  }
  return conf

 def webspheredecode(self,data,options):
  # remove {xor} if it exists
  pw=data

  if data[:5] == "{xor}":
   pw=data[5:]

  pw=base64.b64decode(pw)

  out=''
  for a in pw:
   out+=chr(ord(a) ^ 0x5f)
  return out
