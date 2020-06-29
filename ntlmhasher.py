#!/usr/bin/env python2

# Provide the password you want to convert to an NTLM hash as an argument
# Usage: ./ntlmhasher.py password

import hashlib,binascii,sys

if len(sys.argv) != 2:
    print("[*] Usage {} <password_to_hash>".format(sys.argv[0]))
    exit(1)

password = sys.argv[1]
hash = hashlib.new('md4', password.encode('utf-16le')).digest()
print(binascii.hexlify(hash))
