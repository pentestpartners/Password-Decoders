Some simple password decoders that I've hacked together whilst onsite.

pwdecoder
=========
A generic python plugin runner which contains a host of decodes to put them all in one place. Was written with Python 2.7, but should work with 3. Requires documentation.

decodejenkins.py
================
This will decode credential hashes found in Jenkins config and credentials.xml files. I wrote this as https://github.com/tweksteen/jenkins-decrypt failed to work on the version of Jenkins I was looking at - it appears that some structure changes were put in place in the later versions.

To work it needs the master.key and hudson.util.Secret file from the Jenkins root directory. These are generated per host.

The hash can be identified as it should be surrounded by braces, be base64 encoded and start with "AQAAABAAAAAQ"

wysedecode.c
============
Some very simple and hacked together C to decode a stored Wyse password. This is pretty much a direct translation from the assembly language and probably needs translation to a different language.

It's released under the MIT licence, so feel free to steal it, but be nice and attribute other's work.
