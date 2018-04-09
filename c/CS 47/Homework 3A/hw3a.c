#include <stdio.h>
#include <stdlib.h>

int num;
unsigned int position;

void usage(char* progname) {
  printf("usage: %s <number>\n", progname);
}


void bitsearch() {
   __asm__ ("\
	movl num, %eax\n\
	bsr %eax, %ecx\n\
	movl %ecx, position\n\
");
}



int main(int argc, char* argv[])
{
   if (argc != 2) {
      usage(argv[0]);
      exit(1);
   }
   num = atoi(argv[1]);
   printf("finding the highest bit position in %d (base 10), which is 0x%x (base 16)\n", num, num);




   bitsearch();



   if (position == -1) {
     printf("no one's\n");
   } else {
     printf("bit position: %d\n", position);
   }
   return 0;
}
