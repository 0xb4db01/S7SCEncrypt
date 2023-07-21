# S7SCEncrypt

This is some scripts I made while studying the Sektor7 courses. Nothing really fancy, it's just that they used scripts in Python 2.7 and I wanted to use Python 3.

Generally, the output can be on cli in C friendly format or on file in binary format because my main goal was obviously shellcode encryption.

# Install

A virtualenv is recommended.

```
pip install -r requirements.txt
```

## xorencrypt.py

Encrypt a text message from cli

```
python3 xorencrypt.py -k mysecretkey -m hello
{ 0x5, 0x1c, 0x1f, 0x9, 0xc };
```

Encrypt a file and output to stdout

```
python3 xorencrypt.py -k mysecretkey -i file.txt
{ 0x5, 0x1c, 0x1f, 0x9, 0xc, 0x78 };
```

Encrypt a file and output to file (binary)

```
python3 xorencrypt.py -k mysecretkey -i file.txt -o file.bin
Wrote 6 bytes

xxd file.bin
00000000: 051c 1f09 0c78                           .....x
```

## aesencrypt.py

Encrypt a text message from cli

```
python3 aesencrypt.py -m hello
AES Key        : { 0x23, 0x28, 0xae, 0x93, 0x9c, 0x44, 0x1d, 0x36, 0x7b, 0xf5, 0xf1, 0x3b, 0x92, 0xde, 0xb0, 0xd8 };

AES payload    : { 0x8a, 0xe8, 0x20, 0x34, 0x7e, 0x40, 0x6f, 0x42, 0x89, 0x99, 0xa7, 0xb2, 0x1f, 0xd3, 0xfc, 0x4f };

AES payload len: 16
```

Encrypt a file and output to stdout

```
AES Key        : { 0x57, 0x6e, 0xde, 0xd1, 0xa4, 0x7a, 0x1d, 0xed, 0xf9, 0x1f, 0x8e, 0xaf, 0xfc, 0x73, 0x7b, 0x82 };

AES payload    : { 0xc2, 0xcd, 0xe4, 0x3d, 0x3b, 0x59, 0x2e, 0x5b, 0x52, 0xdd, 0xa4, 0x40, 0x24, 0x30, 0x7d, 0xdc };

AES payload len: 16
```

Encrypt a file and output to file (binary)

```
python3 aesencrypt.py -i file.txt -o file.bin
AES Key        : { 0x82, 0x99, 0x48, 0xfd, 0x2a, 0xf7, 0xba, 0xa9, 0x1, 0x3, 0x3f, 0x3b, 0x61, 0x13, 0xa5, 0xaf };
Wrote 16 bytes in file.bin

xxd file.bin
00000000: 109b 9acf decf 18e1 74c1 e925 099c 3a7a  ........t..%..:z
```

## bin2hfile.py

Generate a C/C++ header file from a binary data file. Assuming you have created a file with aesencrypt.py which contains a shellcode, you can turn it into a formatted header file

```
python3 bin2hfile.py -i file.bin -o file.h -l 207376
```

where -i is the input file, -o is the header file you wish to create and -l is the length of the payload.
