#!/usr/bin/python

import binascii

class cisco(object):

 def __init__(self):
  self.key="dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87" 

 def init(self):
  conf={
   'name':'cisco',
   'author':'tautology',
   'hashes':[
    {
     'name': '7',
     'decode': self.type7decode,
    }
   ]
  }
  return conf

 def type7decode(self,data,option):
  # get the salt
  salt=int(data[:2])
  result=""
  keylen=len(self.key)

  for i, value in enumerate(bytearray.fromhex(data[2:])):
   result+=chr(value ^ ord(self.key[(salt+i) % keylen]))
  return result
 
