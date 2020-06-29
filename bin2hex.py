#!/usr/bin/env python2

# Converts binary/shellcode to hex
# Output can be in C or .NET friendly format
# Usage: ./bin2hex.py <c or net> <raw.bin> <output_file.txt>


import sys
import binascii

valid_options = ["c","net"]
count = 0
bytes = 0
sc = ''

if len(sys.argv) != 4 or sys.argv[1].lower() not in valid_options:
    print('[!] Usage: {} <c or net> <raw.bin> <output_file.txt>'.format(sys.argv[0]))
    exit(1)

format = sys.argv[1]

with open(sys.argv[2]) as file:
    data = binascii.hexlify(file.read())
    hexlist = map(''.join, zip(data[::2], data[1::2]))
    for hex in hexlist:
        if count % 16 == 0:
            if format == 'net': sc += "\n0x{},".format(hex)
            else: sc += "\n\"\\x{}".format(hex)
        elif count % 16 == 15 and format != 'net':
            sc += '"'
        else: sc += "0x{},".format(hex) if format == 'net' else "\\x{}".format(hex)
        bytes += 1
        count += 1
    if format == 'net':
        sc = sc[:-1] + '\n'
    else:
        sc += '"\n'
    output = open(sys.argv[3], 'w')
    output.write(sc)
    output.close()

print("[*] Output saved to: {}".format(sys.argv[3]))
if format == 'net': print('[*] .NET format selected - use with \'byte[] buf = new byte[] { hex };\'')
else: print('[*] C format selected - use with \'unsigned char buf[] = "hex";\'')
print("[*] Size of bytes: {}".format(bytes))
