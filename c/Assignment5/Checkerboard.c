/* 
 * File:   Checkerboard.c
 * Author: Han Bao Quan
 *
 * Created on October 12, 2010, 7:18 PM
 */

#include <stdio.h>
#include <string.h>


int charPosition;
int currentColumn;
int currentRow;
int currentLine;

int main()
{

    for (currentRow = 0; currentRow < 8; currentRow++)
    {
        for (currentColumn = 0;currentColumn<8; currentColumn++)
        {
            printf("+");
            for (charPosition = 0; charPosition < 5; charPosition++)
            {
                printf("-");
            }
        }
        printf("+\n");

        for (currentLine = 0; currentLine < 3; currentLine++)
        {
            for (currentColumn = 0;currentColumn<8; currentColumn++)
            {
                printf("|");
                for (charPosition = 0;charPosition< 5; charPosition++)
                {
                    printf(" ");
                }
            }
            printf("|\n");
        }
    }

    for (currentColumn = 0;currentColumn<8; currentColumn++) {
        printf("+");
        for (charPosition = 0; charPosition<5; charPosition++)
        {
            printf("-");
        }
    }
    printf("+\n");

    return(0);
}







