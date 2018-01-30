#!/usr/bin/env python

from pike.manager import PikeManager
import sys,argparse
import string

plugins=[]

def syntax():
 print("Syntax: pwdecode -m hashtype hash");

def listplugins():
 for plugin in plugins:
  print("Name: " + plugin['name'])
  print("Author: " + plugin['author'])
  print("Hashes supported:")
  for hash in plugin['hashes']:
   if plugin['name'] == hash['name']:
	print (" "+plugin['name'])
   else:
    print(" "+plugin['name']+"."+hash['name'])
  print

def initplugins():
 with PikeManager([plugin_path]) as mgr:
  classes=mgr.get_classes()

  for item in classes:
   obj=item()
   plugins.append(obj.init())

if __name__ == "__main__":
 plugin_path = 'plugins'
 initplugins()
 pluginopts={}

 # frig for --list
 if len(sys.argv) > 1:
  if sys.argv[1] == '-l' or sys.argv[1] == '--list':
   listplugins()
   exit(0)
  
 parser=argparse.ArgumentParser(description='Decode encoded hashes.')
 parser.add_argument('--options','-O')
 parser.add_argument('--list','-l')
 parser.add_argument('type')
 parser.add_argument('hash')
 args=parser.parse_args()

 # if options are provided split them up
 if args.options:
  opts=string.split(args.options,",")
  for opt in opts:
   equals=string.find(opt,'=')
   if equals > 0:
    pluginopts[opt[:equals]]=opt[equals+1:]
   else:
    pluginopts[opt]=True
  
 if string.find(args.type,'.') > 0:
  typeclass=string.split(args.type, '.')[0]
  typehash=string.split(args.type, '.')[1]
 else:
  typeclass=typehash=args.type
 
 typefound=0

 for plugin in plugins:
  if plugin['name']==typeclass:
   for mhash in plugin['hashes']:
    if mhash['name'] == typehash:
     print(mhash['decode'](args.hash, pluginopts))
     typefound=1

 if not typefound:
  print "Unknown hash type: " + args.type + " (expanded as " + typeclass + "." + typehash + ")"
