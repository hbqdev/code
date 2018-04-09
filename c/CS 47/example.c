#include <stdio.h>
#include <stdlib.h>

int i;

void usage() {
  printf("hey, supposed to supply an integer argument\n");
}

int main(int argc, char* argv[]) {

  if (argc != 2) {
    usage();
    exit(1);
  }

  i = atoi(argv[1]);


  __asm__("					\
	movl i, %eax\n\
        imull $53, %eax\n\
	movl %eax, i\n\
  ");

  printf("after multiply, value is %d\n", i);

  return 0;
}
