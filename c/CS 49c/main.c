#include <stdio.h>
#include <string.h>

/*
    Prints a checker board (8-by-8 grid).  Each square will be 5-by-3
    characters wide.  This is surprisingly tough to generalize.
*/

/* These facilitate getting options from a prompt */

char input[80];            /* A line of input from the keyboard */

/* Some parameters for the checker board */

int squareWidth;           /* Width of a square */
int squareHeight;          /* Height of a square */
int numSquaresWide;        /* Width of checker board in squares */
int numSquaresHigh;        /* Height of checker board in squares */

/* Various counters for use in loops */

int charPosition;          /* The cursor position relative to the square */
int currentColumn;         /* The column number we're working on */
int currentRow;            /* The row number we're working on */
int currentLine;           /* The line number we're working on */

int main() {
    printf("Enter:  width height numberWide numberHigh:  ");
    fgets(input, sizeof(input), stdin);
    sscanf(input, "%d %d %d %d", &squareWidth, &squareHeight, 
        &numSquaresWide, &numSquaresHigh);

    for (currentRow = 0; currentRow < numSquaresHigh; ++currentRow) {

/* Print the dashed top lines */

        for (currentColumn = 0; 
            currentColumn < numSquaresWide; ++currentColumn) {
            printf("+");
            for (charPosition = 0; charPosition < squareWidth; ++charPosition) {
                printf("-");
            }
        }
        printf("+\n");

/* Print the lines in the middle that just contain | (pipe) characters */

        for (currentLine = 0; currentLine < squareHeight; ++currentLine) {
            for (currentColumn = 0;
                currentColumn < numSquaresWide; ++currentColumn) {
                printf("|");
                for (charPosition = 0; 
                    charPosition < squareWidth; ++charPosition) {
                    printf(" ");
                }
            }
            printf("|\n");
        }
    }

/* Print the final bottom line */

    for (currentColumn = 0; 
        currentColumn < numSquaresWide; ++currentColumn) {
        printf("+");
        for (charPosition = 0; charPosition < squareWidth; ++charPosition) {
            printf("-");
        }
    }
    printf("+\n");
    return(0);
}


