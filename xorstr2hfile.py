from sys import argv
from getopt import getopt
from xorencrypt import xorro

##
# C Header file with XORed variables generator
# Author: 0xb4db01
# date: 24-Jul-2023
#

##
# Generate C code for an unsigned char variable
#
# @param varname variable name
# @param key XOR key
# @param data variable value
# @return unsigned char c code
#
def gen_enc_str(varname: str, key: str, data: bytes) -> str:
    return 'unsigned char ' + varname + '[] = { ' + ', '.join(hex(i) for i in xorro(key, data)) + ' };'

##
# Parse file for lines such as "variable_name,variable_value"
#
# @param filename text file with variable definitions
# @return dict of tuples with variable name and value
#
def parse_file(filename: str) -> dict:
    variables = []

    with open(filename, 'r') as f:
        for line in f.readlines():
            try:
                varname, data = line.strip().split(',')
                variables.append((varname, data))
            except Exception as e:
                print('Malformed line...')

                continue

    return variables

##
# Generate C header file
#
# @param filename C header file name
# @param variables dict generated with parse_file function
# @key XOR key
#
def gen_header_file(filename: str, variables: dict, key: str):
    with open(filename, 'w') as f:
        f.write('#define XORKEY "' + key + '"\n\n')

        for i in variables:
            f.write(gen_enc_str(i[0], key, i[1].encode()))
            f.write('\n')
            f.write('size_t ' + i[0] + '_len = ' + str(len(i[1])) + ';\n\n')

def main():
    opts, args = getopt(argv[1:], 'k:i:o:')

    key = None
    input_file = None
    output_file = None

    for opt in opts:
        if opt[0] == '-k':
            key = opt[1]

        if opt[0] == '-i':
            input_file = opt[1]

        if opt[0] == '-o':
            output_file = opt[1]

    if input_file is None or output_file is None or key is None:
        print('args: -k <xor key> -i <input file> -o <output file>')

        exit(-1)

    variables = parse_file(input_file)
    
    gen_header_file(output_file, variables, key)

if __name__ == '__main__':
    main()
