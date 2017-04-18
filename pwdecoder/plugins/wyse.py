#!/usr/bin/python

class wyse(object):

 def init(self):
  conf={
   'name':'wyse',
   'author':'tautology',
   'hashes':[
    {
     'name': 'wyse',
     'decode': self.wysedecode,
    }
   ]
  }
  return conf

 def base26(self,data):
  out=bytearray('')
  for a, b in zip(data[0::2], data[1::2]):
   r=ord(a)-1
   r<<=4
   r&=0xff
   r+=ord(b)
   r-=0x41
   r&=0xff
   out.extend(chr(r))
  return out

 def xorit(self,data):
  out=bytearray('')
  a=0
  for i in range(-1, len(data)-1):
   a^=data[i+1]
   a^=0xa5
   out.extend(chr(a))
   a=data[i+1]
  return out 
 
 def wysedecode(self,data,options):
   return self.xorit(self.base26(data))
 
