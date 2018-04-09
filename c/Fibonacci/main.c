/* 
 * File:   main.c
 * Author: hanbaoquan
 *
 * Created on October 21, 2010, 3:48 PM
 */

#include <stdio.h>
#include <stdlib.h>

/*
 * 
 */
int i;
int sum;
int Fibonacci(int x)
{
    if(x<=2)
        return 1;
    else
        return Fibonacci(x-1)+Fibonacci(x-2);
}
int main(int argc, char** argv)
{
        printf("%d\n", Fibonacci(7));
 
}

