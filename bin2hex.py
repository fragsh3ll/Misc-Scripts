#!/usr/bin/env python2

# Converts binary/shellcode to hex
# Can be delimited by "0x41,0x42" or "\x41\x42" - uncomment the format you want 
# Usage: ./bin2hex.py <raw.bin> <output_file.txt>

import sys
import binascii

bytes = 0
sc = ''

if len(sys.argv) != 3:
    print('[!] Usage: {} <raw.bin> <output_file.txt>'.format(sys.argv[0]))
    exit(1)

with open(sys.argv[1]) as file:
    data = binascii.hexlify(file.read())
    hexlist = map(''.join, zip(data[::2], data[1::2]))
    for hex in hexlist:
        sc += "0x{},".format(hex) # format = 0x41,0x42,0x43,0x44...
        #sc += "\\x{}".format(hex) # format = \x41\x42\x43\x44...
        bytes += 1
    sc = sc[:-1]
    output = open(sys.argv[2], 'w')
    output.write(sc)
    output.close()

print("[*] Output saved to: {}".format(sys.argv[2]))
print("[*] Size of bytes: {}".format(bytes))
