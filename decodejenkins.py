#!/usr/bin/env python

import binascii
import getopt
import base64
import struct
import sys
from Crypto.Cipher import AES
from hashlib import sha256

unpad = lambda s : s[0:-ord(s[-1])]

def main(argv):
	masterfile=''
	secretfile=''
	hash=''
	keys={}
	syntax="decodejenkins -m master.key -s hudson.util.Secret -a <hash>"
	
	try:
		opts, args = getopt.getopt(argv,"hm:s:a:")
	except getopt.GetoptError:
		print syntax
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print syntax
			sys.exit()
		elif opt in ("-m", "--master"):
				masterfile = arg
		elif opt in ("-s", "--secret"):
				secretfile = arg
		elif opt in ("-a", "--hash"):
				hash = arg
	
	if masterfile == '' or secretfile == '' or hash == '':
		missing="Missing "
		missing+="master key, " if masterfile=='' else ""
		missing+="secret key, " if secretfile=='' else ""
		missing+="hash" if hash=='' else ""
		print missing
		print syntax
		sys.exit(2)
		 
	try:
		master=open(masterfile,"rb").read()
	except:
		print "Could not open " + masterfile
		sys.exit(3)
	keys['master']=sha256(master).digest()[:16]
	  
	try:
		secret=open(secretfile,"rb").read()
	except:
		print "Could not open " + secretfile
		sys.exit(4)
	o=AES.new(keys['master'], AES.MODE_ECB)
	keys['secret']=o.decrypt(secret)[:16]
	
	# Now to read the hash - first break it up
	try:
		cooked=base64.b64decode(hash)
	except base64.TypeError:
		print "Hash does not appear to be valid base64"
		sys.exit(5)
	  
	if cooked[0] == '\x01':
		# We have a valid hash (maybe)
		ivlen=struct.unpack('>i',cooked[1:5])[0]
		dlen=struct.unpack('>i',cooked[5:9])[0]
		# Sanity check
		if ivlen % 16 != 0:
			print "iv length on hash needs to be a multiple of 16: " + ivlen
			sys.exit(5)
		if dlen % 16 != 0:
			print "data length on hash needs to be a multiple of 16: " + dlen
			sys.exit(5)
		istart=9
		iend=9+ivlen
		dstart=iend
		dend=dstart+dlen
		iv=cooked[istart:iend]
		crypted=cooked[dstart:dend]

		# Right, now we can decode the bugger
		c=AES.new(keys['secret'], AES.MODE_CBC, iv)
		pw=c.decrypt(crypted)
		print "Password is " + unpad(pw)
	else:
		print "Invalid hash found"
		sys.exit(5)

if __name__ == "__main__":
	main(sys.argv[1:])		