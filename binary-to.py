# Copyright is waived. No warranty is provided. Unrestricted use and modification is permitted.

import sys
import base64
import hashlib
import binascii

PURPOSE = '''\
Convert a binary file to a text format or a hash

binary-to.py <output_type> <input_file> [<struct_name>]

where,
   <output_type>   base32, base64, base64url, c, cpp, crc32, hex, java, md5, python, sha1, sha256 
   <input_file>    Path to input file
   <struct_name>   Name to give output structure (if applicable)
'''

if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.exit(PURPOSE)

    output_type = sys.argv[1].lower()
    with open(sys.argv[2], 'rb') as f:
        data = f.read()

    if output_type in ['c', 'cpp']:
        index = 0
        struct_name = sys.argv[3] if len(sys.argv) > 3 else 'struct_name'
        output = 'unsigned char ' + struct_name + '[] = {\n'
        while index < len(data):
            output += '\t'
            row_length = len(data) - index
            row_length = 16 if row_length > 16 else row_length
            for i in range(row_length):
                output += '0x%02x, ' % data[index]
                index += 1
            output += '\n'
        output = output[:-3] + '\n};\n'
        print(output)

    elif output_type == 'base32':
        print(base64.b32encode(data).decode('latin_1'))

    elif output_type == 'base64':
        print(base64.b64encode(data).decode('latin_1'))

    elif output_type == 'base64url':
        print(base64.urlsafe_b64encode(data).decode('latin_1'))

    elif output_type == 'crc32':
        print('{0:08x}'.format(binascii.crc32(data) & 0xffffffff))

    elif output_type == 'hex':
        print(data.hex())

    elif output_type == 'java':
        index = 0
        array_name = sys.argv[3] if len(sys.argv) > 3 else 'array_name'
        output = 'byte ' + array_name + '[] = {\n'
        while index < len(data):
            output += '\t'
            row_length = len(data) - index
            row_length = 16 if row_length > 16 else row_length
            for i in range(row_length):
                value = data[index]
                if value >= 128:
                    value -= 256
                output += '%4d, ' % value
                index += 1
            output += '\n'
        output = output[:-3] + '\n};\n'
        print(output)

    elif output_type == 'md5':
        print(hashlib.md5(data).hexdigest())

    elif output_type == 'python':
        index = 0
        var_name = sys.argv[3] if len(sys.argv) > 3 else 'array_name'
        output = var_name + ' = bytearray([\n'
        while index < len(data):
            row_length = len(data) - index
            row_length = 16 if row_length > 16 else row_length
            for i in range(row_length):
                output += '%4d, ' % data[index]
                index += 1
            output += '\n'
        output = output[:-3] + '\n])\n'
        print(output)

    elif output_type == 'sha1':
        print(hashlib.sha1(data).hexdigest())

    elif output_type == 'sha256':
        print(hashlib.sha256(data).hexdigest())
