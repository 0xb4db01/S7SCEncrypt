from sys import argv
from getopt import getopt

##
# Author     : 0xb4db01
# Description: XOR encrypts either a file or a message.
# File encryption can be printed out in a C friendly format or saved in
# a binary file.
# Message encryption is only printed out in a C friendly format.
# 
# This is something I did while studying sektor7 courses because I didn't
# want to stick with good ol' python2.7. I strongly doubt this can be useful
# out of shellcode encryption
#

##
# @description XOR encrypt
# @param key xor key
# @param msg the data to encrypt
#
def xorro(key: str, msg: bytes):
    return bytearray([msg[i] ^ ord(key[i % len(key)]) for i in range(0, len(msg))])

##
# @description Encrypt a message in a C format such as { 0xaa, 0xbb, ...};
# @param key xor key
# @param msg message to encrypt
#
def c_fmt(key: str, msg: bytes):
    print('payload    :{ ' + ', '.join(hex(i) for i in xorro(key, bytes(msg))) + ' };')
    print('\n')
    print('payload len:', len(msg))

##
# @description Encrypt a file
# @param ifile input file
# @param ofile output file
# @key xor key
#
def encrypt_file(ifile: str, ofile: str, key: str):
    with open(ifile, 'rb') as ifile_h:
        with open(ofile, 'wb') as ofile_h:
            n = ofile_h.write(xorro(key, ifile_h.read()))

            print(f'Wrote {n} bytes'.format(n=n))

if __name__ == '__main__':
    opts, args = getopt(argv[1:], 'k:i:o:m:')

    ifile = None
    ofile = None
    key = None
    msg = None

    for opt in opts:
        if opt[0] == '-k':
            key = opt[1]

        if opt[0] == '-i':
            ifile = opt[1]

        if opt[0] == '-o':
            ofile = opt[1]

        if opt[0] == '-m':
            msg = opt[1]

    if key and msg and ifile is None and ofile is None:
        c_fmt(key, msg.encode())

    elif key and ifile and ofile and msg is None:
        encrypt_file(ifile, ofile, key)

    elif key and ifile and ofile is None and msg is None:
        c_fmt(key, open(ifile, 'rb').read())

    else:
        print('args: -k <key> [-m <message> OR -i <input file> [ -o <output file>] ]')

        exit(-1)
