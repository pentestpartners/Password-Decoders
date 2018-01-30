#!/usr/bin/python

# Sofia password demangler, stolen from https://github.com/tothi/pwn-hisilicon-dvr
import hashlib

class sofia(object):

 def init(self):
  conf={
   'name':'sofia',
   'author':'tautology, stolen from tothi',
   'hashes':[
    {
     'name': 'sofia',
     'decode': self.sofiadecode,
    }
   ]
  }
  return conf

 def sofiadecode(self,data,options):
  h=""
  m=hashlib.md5()
  m.update(data)
  msg_md5=m.digest()
  for i in range(8):
   n=(ord(msg_md5[2*i]) + ord(msg_md5[2*i+1])) % 0x3e
   add=48
   if n > 9:
    if n > 35:
     add=61
    else:
     add=55
   n+=add
   h+=chr(n)

  return h
