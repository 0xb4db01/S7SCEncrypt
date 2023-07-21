from sys import argv
from Crypto.Cipher import AES
from os import urandom
import hashlib
from getopt import getopt

##
# Author     : 0xb4db01
# Description: AES encrypts a file or a message. Key is generated randomly.
# If you encrypt a file, you can either output a C friendly format or save to
# an output file in binary form.
# If you encrypt a message you get only a C friendly format on stdout.
# As output you will always get the key in C friendly format.
# 
# This is something I did while studying sektor7 courses because I didn't
# want to stick with good ol' python2.7. I strongly doubt this can be useful
# out of shellcode encryption
#

KEY = urandom(16)

##
# @description Get the message encrypted in C friendly format
# @param data message
#
def get_c_fmt(data: bytes) -> bytes:
    return '{ 0x' + ', 0x'.join(hex(x)[2:] for x in data) + ' };'

##
# @description AES padding
# @param data message
#
def pad(data: bytes) -> bytes:
    x = bytearray(data)

    return data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size).encode()

##
# @description AES Encrypt data (IV is all zeroes, not good but ok for me)
# @param data the data to encrypt
#
def encrypt(data: bytes) -> bytes:
    k = hashlib.sha256(KEY).digest()
    iv = 16 * '\x00'

    data = pad(data)

    cipher = AES.new(k, AES.MODE_CBC, iv.encode())

    return cipher.encrypt(bytes(data))

##
# @description AES encrypt file
# @param ifile the input file
# @param ofile the output file
#
def encrypt_file(ifile: str, ofile: str) -> None:
    f = open(ifile, 'rb')

    file_content = f.read()

    f.close()

    encrypted = encrypt(file_content)

    print('AES Key        :', get_c_fmt(KEY))

    f = open(ofile, 'wb')

    n = f.write(encrypted)

    f.close()

    print('Wrote %d bytes in %s' % (n, ofile))

##
# @description encrypt a message
# @param msg the message to encrypt
#
def encrypt_message(msg: bytes) -> None:
    encrypted = encrypt(msg)

    print('AES Key        :', get_c_fmt(KEY), '\n')
    print('AES payload    :', get_c_fmt(encrypted), '\n')
    print('AES payload len:', len(encrypted))

if __name__ == '__main__':
    ifile = None
    ofile = None
    msg = None

    opts, args = getopt(argv[1:], 'i:o:m:')

    for opt in opts:
        if opt[0] == '-i':
            ifile = opt[1]

        if opt[0] == '-o':
            ofile = opt[1]

        if opt[0] == '-m':
            msg = opt[1]

    if ifile and ofile and msg is None:
        encrypt_file(ifile, ofile)
    elif ifile and ofile is None and msg is None:
        encrypt_message(open(ifile, 'rb').read())
    elif msg and ifile is None and ofile is None:
        encrypt_message(msg.encode())
    else:
        print('args: -i <input filename> [ -o <output filename> ] OR -m <message>')

        exit(-1)
