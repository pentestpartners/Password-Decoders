#!/usr/bin/python

import base64
import struct

class lansweeper(object):

 def init(self):
  conf={
   'name':'lansweeper',
   'author':'tautology',
   'hashes':[
    {
     'name': 'lansweeper',
     'decode': self.lansweeperdecode,
    }
   ]
  }
  return conf

 # XTEA for python stolen shamelessly from Paul Chakravarti
 # (http://code.activestate.com/recipes/496737-python-xtea-encryption/)
 def crypt(self,key,data,iv='\00\00\00\00\00\00\00\00',n=32):
  def keygen(self,key,iv,n):
   while True:
    iv = self.xtea_encrypt(key,iv,n)
    for k in iv:
     yield ord(k)
  xor = [ chr(x^y) for (x,y) in zip(map(ord,data),self.keygen(key,iv,n)) ]
  return "".join(xor)

 def xtea_encrypt(self,key,block,n=32,endian="!"):
  v0,v1 = struct.unpack(endian+"2",block)
  k = struct.unpack(endian+"4",key)
  sum,delta,mask = 0,0x9e3779b9,0xffffffff
  for round in range(n):
   v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
   sum = (sum + delta) & mask
   v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
  return struct.pack(endian+"2",v0,v1)

 def xtea_decrypt(self,key,block,n=32,endian="!"):
  v0,v1 = struct.unpack(endian+"2",block)
  k = struct.unpack(endian+"4",key)
  delta,mask = 0x9e3779b9,0xffffffff
  sum = (delta * n) & mask
  for round in range(n):
   v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
   sum = (sum - delta) & mask
   v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
  return struct.pack(endian+"2",v0,v1)

 def makesalt(self):
  key=''
  for x in range(0,61):
   key += chr(((40 - x) + ((x*2) + x)) -1) 
   key += chr(x + 15 + x)
  return key

 def lansweeperdecode(self,data,options):
  pw=base64.b64decode(data)

  key=pw[1:9]
  crypted=pw[9:]
  c=''

  key=(key + self.makesalt())[:16]

  for i in [crypted[x:x+8] for x in range(0, len(crypted), 8)]:
   c+=self.xtea_decrypt(key, i, endian='<')
  return c
