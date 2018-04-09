#include <stdio.h>
#include <string.h>

/*
    A program to compute the area and perimeter of a rectangle with a
    width of three inches and a height of five inches.  What changes must
    be made to the program so that it works for a rectangle with width
    of 6.8 inches and length of 2.3 inches?
*/

float height;     /* Height of the rectangle, in inches. */
float width;      /* Width of the rectangle, in inches. */
float perimeter;  /* Perimeter of the rectangle, in inches. */
float area;       /* Area of the rectangle, in square inches. */
char input[90];
int i;
float num1;
float num2;
char dim[80];
int main()
{
    while(1)
    {
    printf("Please enter dimensions: ");
    fgets(input, sizeof(input), stdin);
    input[strlen(input)-1] = '\0';
    sscanf(input,"%f %f", &num1, &num2);
    width = num1;
    height = num2;
    perimeter = (2 * height) + (2 * width);
    area = height * width;
    printf("Rectangle:  height %f, width %f\n", height, width);
    printf("Area:  %-5f, Perimeter:  %-5f\n", area, perimeter);
    if(strcmp(input,"quit")==0)
        break;
    }
    return 0;
}
