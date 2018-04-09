/* 
 * File:   main.c
 * Author: Han Bao Quan
 *
 * Created on February 1, 2011, 11:16 PM
 * I worked with Zane Melcho
 */

#include <stdio.h>
#include <stdlib.h>

/*
 * 
 */
/* declare two global variables */
int num;
int mask;

/* a helper function to print out a number in binary */
void print32bits(int x)
{

   unsigned int mask;       /* declare as a local variable */

   mask = 0x80000000;       /* initializes the local, not global mask */
   while (mask != 0)
   {
      if ((mask & x) == 0)
         printf("0");
      else
         printf("1");
      mask = mask >> 1;
   }
   printf("\n");
}


int get_bits_squeeze(int num, int mask) 
    { 
       unsigned int mask2 = 0x80000000; 
       int num2 = 0; 
        
       while (mask2 != 0) 
       { 
         if ((mask & mask2) == 0)  
         { 
           num2 = num2 >> 1; 
         } 
         else if ((mask2 & num)!= 0) 
         { 
           num2 = num2 ^ mask2; 
         } 
             
         mask2 = mask2 >> 1;     
       } 
       return num2; 
    } 

/*
   the main function. argc, argv are the command-line arguments,
   like args in Java
*/
int main(int argc, char* argv[])
{
   int result;                  /* declare a local variable */

   num = atoi(argv[1]);		/* store first command line argument into num */
   mask = atoi(argv[2]);	/* store second into mask */
   print32bits(num);		/* produce first line of output */
   print32bits(mask);		/* produce second line of output */
   result = get_bits_squeeze(num, mask);
   print32bits(result);		/* produce third line of output */
   exit(0);                     /* success */
}

