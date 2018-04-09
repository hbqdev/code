/*
 * File:   newmain.c
 * Author: Tin Tran
 *
 * Created on September 14, 2010, 8:59 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 *
 */

int comma;

int num1;
int num2;
char*stringnum;
char*string1;
char*string2;
int Primeon = 1;
int Perfecton =1;
int i;
int main()
{
    char str[256];

    while(1)
    {
    printf("Please enter the command here: ");
    fgets(str, sizeof(str), stdin);
    str[strlen(str)-1] = 0;
    for (i=0; i<strlen(str); i++)
    {
        if((str[i]>= 'A')&&(str[i] <='Z'))
            str[i] = str [i] +'a'-'A';
    }
    if(strcmp(str, "prime")==0)
    {
            Primeon = 1 - Primeon;
            printf("Prime report is %d\n",Primeon);
    }
    if(strcmp(str,"perfect")==0)
    {
        Perfecton = 1 - Perfecton;
        printf("Perfect report is %d\n", Perfecton);
    }

    if(strcmp(str, "quit")==0)
    {
        break;
    }

    if(strcmp(str,"help")==0)
    {
        printf("Please refer to your book for more information\n");
    }

    else
    {
        int x =1;

        stringnum = strtok(str, ",");
        string1 = ("i : %s\n", x, stringnum);
        stringnum = strtok(NULL, ",");
        string2 = stringnum;
        if(sscanf(string1, "%d", &num1)==1)
        {
           if(sscanf(string2, "%d", &num2)==1)
            {

                findPrime(num1,num2);

                findPerfect(num1,num2);

            }
        }

    }
}


    return (0);
}

int isPrime(int num)
{
    int i;

    if(num<2)
    {
        return 0;
    }
    for(i=2;i<num;i++)
    {
       if(num%i==0)
        {
            return 0;
            break;
        }
    }
        if(i==num);
        {
            //printf("The number is prime\n");
           return 1;

        }



}

int isPerfect(int num)
{
    int i;
    int sum =0;
    for (i=1;i<num;i++)
    {
        int c = num%i;
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
void findPrime(int start, int end)
{
    int i;
    if(Primeon == 1)
    {
      for (i = start; i<=end;i++)
        {
           if(isPrime(i)==1)
            {
                printf("The Prime number is %d\n", i);
            }
        }
    }
    else
        printf("Prime report is off\n");
    }

void findPerfect(int start, int end)
{
    int i;
    if(Perfecton == 1)
    {
    for(i=start; i<=end;i++)
    {
        if(isPerfect(i)==1)
        {
            printf("The perfect number is %d\n", i);
        }
    }
    }
    else
        printf("Perfect report is off\n");

}




