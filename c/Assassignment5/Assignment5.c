/*
 * File:   main.c
 * Author: hanbaoquan
 *
 * Created on September 21, 2010, 3:37 PM
 */

#include <stdio.h>
#include <string.h>

char input[80];
int i;
int comma;
int j;
int ErrorFound;
int firstnum;
int secondnum;
char input[80];            

int squareWidth = 7;
int squareHeight = 3;
int numSquaresWide = 8;
int numSquaresHigh = 8;

char roco[80];
int charPosition;          
int currentColumn;         
int currentRow;            
int currentLine;           
int num;
int i;
int data[40][40];

char BSR0[7];
    char BSR1[7];
    char BSR2[7];
    char BSR3[7];
    char BSR4[7];


    char BXR0[7];
    char BXR1[7];
    char BXR2[7];
    char BXR3[7];
    char BXR4[7];
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
    /*if(strlen(input)==0)
    {
        numSquaresHigh = numSquaresHigh;
        numSquaresWide = numSquaresWide;
    }*/
    sscanf(input, "%s %d", &roco, &num);
    if(strcmp(roco, "rows")==0)
    {
        printf("setting row to %d\n", num);
        numSquaresHigh = num;
        PrintBoard();
        continue;printf("Input range to check amicable numbers: ");
    }
    if(strcmp(roco, "columns")==0)
    {
        printf("setting column to %d\n", num);
        numSquaresWide = num;
        PrintBoard();
        continue;
    }
    else if(strcmp(input,"quit")==0)
    {
        break;
    }
    else if(strcmp(input,"help")==0)
    {
        printf("Please refer to the textbook for more info\n");
        continue;
    }
    else
    {
   for(i=0;i<strlen(input);i++)
    {
        if (input[i] == ',')
        //comma = i;
        break;
    }
    printf("Comma is found at %d\n",i);
    if(i == strlen(input) && strlen(input)==0)
    {
        PrintBoard();
        continue;
        //printf("Error: Comma not foud\n");
        //ErrorFound=1;
    }
    firstnum =0;
    for(j=0; j<i;j++)
    {
        firstnum = input[j]-'0'+10*firstnum;
        if((input[j]>'9')||(input[j]<'0'))
        {
            printf("Error, Invalid command\n");
            ErrorFound=1;
        }
    }
    secondnum=0;
    for(j=i+1; j<strlen(input);j++)
    {
        secondnum=input[j]-'0'+10*secondnum;
        if((input[j]>'9')||(input[j]<'0'))
        {
            printf("Error, invalid command\n");
            ErrorFound=1;
        }
    }

        if (ErrorFound ==1)
        {
            PrintBoard();
            continue;
        }
     
    }
    //printf("%d %d\n", firstnum, secondnum);
    data[firstnum-1][secondnum-1]=1-(data[firstnum-1][secondnum-1]);
    PrintBoard();
        
    }
     return(0);
    }
     

void PrintBoard()
{
    strcpy(BSR0, "+-----+");
    strcpy(BSR1, "|     |");
    strcpy(BSR2, "|     |");
    strcpy(BSR3, "|     |");
    strcpy(BSR4, "+-----+");

    strcpy(BXR0, "+-----+");
    strcpy(BXR1, "|\\\\ //|");
    strcpy(BXR2, "| xxx |");
    strcpy(BXR3, "|// \\\\|");
    strcpy(BXR4, "+-----+");
    
     for (currentRow = 0; currentRow < numSquaresHigh; ++currentRow)
        {
        BSR0[0] = '+';
        printf("%c", BSR0[0]);
        for (currentColumn = 0;
            currentColumn < numSquaresWide; ++currentColumn)
        {
            //printf("%s", BSR0);

            for (charPosition = 1; charPosition < squareWidth; ++charPosition) {
                printf("%c", BSR0[charPosition]);
            }
            //printf("\n");
        }
        printf("\n");


        for (currentLine = 0; currentLine < squareHeight; ++currentLine)
        {
            BSR1[0] = '|';
            BXR1[0] = '|';
            BXR2[0] = '|';
            BXR3[0] = '|';
            printf("%c", BSR1[0]);
            for (currentColumn = 0;
                currentColumn < numSquaresWide; ++currentColumn)
                {

                //printf("%s", BSR1);
                for (charPosition = 1;charPosition < squareWidth; ++charPosition)
                {
                    if(data[currentRow][currentColumn]==0)
                    printf("%c", BSR1[charPosition]);
                    else
                    {
                        switch(currentLine)
                        {
                        case 0: printf("%c", BXR1[charPosition]);break;
                        case 1: printf("%c", BXR2[charPosition]);break;
                        case 2: printf("%c", BXR3[charPosition]);break;
                        default: printf("Error");
                        }
                }
                }
            }
            printf("\n");
            }

            //printf("|\n");
        }
    printf("%c", BSR0[0]);
    for (currentColumn = 0;
        currentColumn < numSquaresWide; ++currentColumn)
    {

        //printf("");
        for (charPosition = 1; charPosition < squareWidth; ++charPosition) {
            printf("%c", BSR0[charPosition]);
        }
    }
    printf("\n");
    }




