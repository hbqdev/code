/* 
 * File:   main.c
 * Author: hanbaoquan
 *
 * Created on October 25, 2010, 9:37 AM
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*
 * 
 */
char input[80];
int i;
int comma;
int j;
int ErrorFound;
int firstnum;
int secondnum;
int main()
{
    while(1)
    {
       
        firstnum =0;
        
        secondnum =0;
        ErrorFound =0;
        
    printf("Enter Command here: ");
    fgets(input, sizeof(input), stdin);
    input[strlen(input)-1] = '\0';
    if(strlen(input)==0)
    {
        printf("Error: Command is empty\n");
        continue;
    }
    if(strcmp(input,"quit")==0)
    {
        break;
    }
    if(strcmp(input,"help")==0)
    {
        printf("Please refer to the textbook for more info");
        continue;
    }
    printf("Command is %s\n", input);
    for(i=0;i<strlen(input);i++)
    {
        if (input[i] == ',')
        //comma = i;
        break;
    }
   
    if(i == strlen(input))
    {
        printf("Error: invalid command");
        ErrorFound=1;
    }
    for(j=0; j<i;j++)
    {
        if((input[j]>'9')||(input[j]<'0'))
        {
            printf("Error, Invalid command");
            ErrorFound=1;
        }
    }
    for(j=i+1; j<strlen(input);j++)
    {
        if((input[j]>'9')||(input[j]<'0'))
        {
            printf("Error, invalid command");
            ErrorFound=1;
        }
    }
    
    if(i ==0 && i ==(strlen(input)-1))
    {
        printf("Error: number is needed");
        ErrorFound =1;
    }
    if(i==strlen(input)-1)
    {
        for(j=0;j<i;j++)
    {
        firstnum = input[j]-'0'+10*firstnum;
    }
        secondnum = (int)pow(2,31)-1;
    }
    else if(i==0)
    {
        firstnum=2;
        for(j=i+1; j<strlen(input);j++)
        {
            secondnum=input[j]-'0'+10*secondnum;
        }
    }
    else
    {
        for(j=0;j<i;j++)
    {
        firstnum = input[j]-'0'+10*firstnum;
    }
        for(j=i+1; j<strlen(input);j++)
        {
            secondnum=input[j]-'0' +10*secondnum;
        }
    }
        if (ErrorFound ==1) continue;
        printf("The two numbers are %d %d\n", firstnum, secondnum);
    }
    
    return (0);
}

