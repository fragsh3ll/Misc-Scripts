#!/usr/bin/env python2

# Converts binary/shellcode to hex
# Output can be in C, Python, or .NET friendly format
# Usage: ./bin2hex.py <c, net, python> <raw.bin> <output_file.txt>


import sys
import binascii

valid_options = ["c","net","python"]
xored_arr = []
count = 0
bytesize = 0
sc = ''

if len(sys.argv) != 4 or sys.argv[1].lower() not in valid_options:
    print('[!] Usage: {} <c, net, python> <raw.bin> <output_file.txt>'.format(sys.argv[0]))
    exit(1)

format = sys.argv[1]

with open(sys.argv[2]) as file:
    data = binascii.hexlify(file.read())
    hexlist = bytearray.fromhex(data)
    for item in hexlist:
        item = '{:02x}'.format(int(item))
        if count % 16 == 0:
            if format == 'net': sc += "\n0x{},".format(item)
            elif format == 'c':  sc += "\n\"\\x{}".format(item)
            else: sc += "\nbuf += b\"\\x{}".format(item)
        elif count % 16 == 15 and format != 'net':
            sc += "\\x{}\"".format(item)
        else: sc += "0x{},".format(item) if format == 'net' else "\\x{}".format(item)
        bytesize += 1
        count += 1
    if format == 'net':
        sc = sc[:-1]
    output = open(sys.argv[3], 'w')
    if format == 'c':
        output.write("\n// Size of bytes: {}\n\nunsigned char buf[] = {}\";\n".format(bytesize,sc))
    elif format == 'net':
        output.write("\n// Size of bytes: {}\n\nbyte[] buf = new byte[] {{ {} }};\n".format(bytesize,sc))
    else:
        output.write("\n// Size of bytes: {}\n\nbuf =  b\"\" {}\"\n".format(bytesize,sc))
    output.close()

print("[*] Output saved to: {}".format(sys.argv[3]))
if format == 'net': print('[*] .NET format selected - use with \'byte[] buf = new byte[] { hex };\'')
elif format == 'c': print('[*] C format selected - use with \'unsigned char buf[] = "hex";\'')
else: print('[*] Python format selected - refer to output file for usage')
print("[*] Size of bytes: {}".format(bytesize))
