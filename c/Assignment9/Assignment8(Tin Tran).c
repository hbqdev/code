/* 
 * File:   main.c
 * Author: hanbaoquan
 *
 * Created on November 16, 2010, 2:11 PM
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
char input[80];

long int range, num, chk, divi, sum, n1, n2,i,j;
int main()
{
    while(1)
    {
  printf("Enter command here: ");
    fgets(input, sizeof(input), stdin);
    input[strlen(input)-1] = '\0';
    for (i=0; i<strlen(input); i++)
    {
        if((input[i]>= 'A')&&(input[i] <='Z'))
            input[i] = input [i] +'a'-'A';
    }
    if(strcmp(input,"quit")==0)
    {
        break;
    }
    if(strcmp(input,"help")==0)
    {
        printf("Please refer to the textbook for more info\n");
        continue;
    }
    if(strlen(input)==0)
    {
        printf("Error: Command not found \n");
    }
    
    else if()
  sscanf(input,"%ld", &range);
  num = 0;
  for(i=1;i<range;i++)
  {
      if(isPerfect(i)==1)
      {
          printf("%d is a perfect number\n",i);
      }
  }
  while ( ++num < range )
  {
            sum = divi = 0;
            while ( ++divi <= num/2 )
            {
                        if ( num % divi == 0 )
                        sum += divi;
            }
            chk = sum;
            sum = divi = 0;
            while ( ++divi <= chk/2 )
            {
                        if ( chk % divi == 0 )
                        sum += divi;
            }
             if ( sum == num )
            {
                        if ( num == chk )
                                    continue;
                        n1 = num;
                        if ( n1 == n2)
                                    continue;
                        n2 = chk;
                        printf("%d %d are amicable numbers\n", n1, n2);
            }
  }

       }
  return 0;
}

int isPerfect(long int num)
{
   long int i;
    long int sum =0;
    for (i=1;i<num;i++)
    {
       long int c = num%i;
        if(c==0)
        {
            sum=sum+i;
        }
    }
    if(sum==num)
    {
        return 1;
    }
    else
        return 0;
}
