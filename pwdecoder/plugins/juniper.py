#!/usr/bin/python

import sys

class juniper(object):

 def __init__(self):
  self.FAMILY = ["QzF3n6/9CAtpu0O", "B1IREhcSyrleKvMW8LXx", "7N-dVbwsY2g4oaJZGUDj", "iHkq.mPf5T"]
  self.EXTRA = dict()
  for x, item in enumerate(self.FAMILY):
   for c in item:
    self.EXTRA[c] = 3 - x
  
  self.NUM_ALPHA = [x for x in "".join(self.FAMILY)]
  self.ALPHA_NUM = {self.NUM_ALPHA[x]: x for x in range(0, len(self.NUM_ALPHA))}
  self.ENCODING = [[1, 4, 32], [1, 16, 32], [1, 8, 32], [1, 64], [1, 32], [1, 4, 16, 128], [1, 32, 64]]

 def init(self):
  conf={
   'name':'juniper',
   'author':'tautology, mangled from a script by matt hite',
   'hashes':[
    {
     'name': '9',
     'decode': self.type9decode,
    }
   ]
  }
  return conf

 def _nibble(self, cref, length):
  nib = cref[0:length]
  rest = cref[length:]
  if len(nib) != length:
   print("Ran out of characters: hit '%s', expecting %s chars" % (nib, length))
   sys.exit(1)
  return nib, rest


 def _gap(self, c1, c2):
  return (self.ALPHA_NUM[str(c2)] - self.ALPHA_NUM[str(c1)]) % (len(self.NUM_ALPHA)) - 1


 def _gap_decode(self,gaps, dec):
  num = 0
  if len(gaps) != len(dec):
   print("Nibble and decode size not the same!")
   sys.exit(1)
  for x in range(0, len(gaps)):
   num += gaps[x] * dec[x]
  return chr(num % 256)

 def juniper_decrypt(self,crypt):
  chars = crypt.split("$9$", 1)[1]
  first, chars = self._nibble(chars, 1)
  toss, chars = self._nibble(chars, self.EXTRA[first])
  prev = first
  decrypt = ""
  while chars:
   decode = self.ENCODING[len(decrypt) % len(self.ENCODING)]
   nibble, chars = self._nibble(chars, len(decode))
   gaps = []
   for i in nibble:
    g = self._gap(prev, i)
    prev = i
    gaps += [g]
   decrypt += self._gap_decode(gaps, decode)
  return decrypt

 def type9decode(self,data,option):
  if data[:3] != "$9$":
   print("Does not look like a type 9 hash")
   sys.exit(1)
  
  return self.juniper_decrypt(data)
 
