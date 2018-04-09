/* 
 * File:   main.c
 * Author: Tin Tran
 *
 * Created on October 20, 2010, 11:18 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
/*
 * 
 */
int num;
char input[80];
int i;
long sum;
char cmd[80];
long Power(int x, int y)
{
    if(y==0)
        return 1;
    else
        return x*Power(x,y-1);
}
long Recurrsion(int x)
{
    if(x==1)
        return 1;
    else
        x-1;
        return Power(x,x)+Recurrsion(x-1);
}

int main()
{
    while(1)
    {
    printf("Enter command here ");
    fgets(input, sizeof(input), stdin);
    input[strlen(input)-1] = '\0';
    for (i=0; i<strlen(input); i++)
    {
        if((input[i]>= 'A')&&(input[i] <='Z'))
            input[i] = input [i] +'a'-'A';
    }
    //sscanf(input, "%s %d", &roco, &num);
    
    if(strcmp(input, "help")==0)
    {
        printf("Please contact the instructor for more instruction \n");

    }
    if(strcmp(input, "quit")==0)
    {
        break;
    }
    if(strlen(input)==0)
    {
        printf("Error: Command not found \n");
    }

    else
    {
               
       sscanf(input,"%d", &num);
       sum = Recurrsion(num);
       printf("The sum is %d \n", sum);
        
    }
    
    }
    return(0);
}

