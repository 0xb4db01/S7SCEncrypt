from getopt import getopt
from sys import argv

def main(input_file: str, output_file: str, payload_len: int) -> None:
    h_input_file = open(input_file, 'rb')
    input_file_data = h_input_file.read()
    h_input_file.close()

    hex_data = '#define PAYLOAD_LEN %d\n\n' % (payload_len)
    hex_data += 'unsigned char payload[] = {\n\t'

    column = 0
    for i in range(0, payload_len):
        if column == 12:
            hex_data += '\n\t'
            
            column = 0

        hex_data += '0x' + format(input_file_data[i], 'x') +', '

        column += 1

    hex_data = hex_data[:-2]

    hex_data += ' };\n'

    h_output_file = open(output_file, 'w')
    h_output_file.write(hex_data)
    h_output_file.close()

    print('Written C/C++ heder file. Payload length:', payload_len)

if __name__ == '__main__':
    opts, args = getopt(argv[1:], 'i:o:l:')

    input_file = None
    output_file = None
    payload_len = None

    for opt in opts:
        if opt[0] == '-i':
            input_file = opt[1]

        if opt[0] == '-o':
            output_file = opt[1]

        if opt[0] == '-l':
            payload_len = int(opt[1])

    if input_file is None or output_file is None or payload_len is None:
        print('args: -i <input file> -o <output file> -l <payload length>')

        exit(-1)

    main(input_file, output_file, payload_len)
