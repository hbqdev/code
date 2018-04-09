#include <stdio.h>

/*
 * A program to convert Centigrade to Fahrenheit.
 */

char inputs[] = {-10, 0, 20, 40};  /* Arbitrary temperatures to convert. */
int outputs[sizeof(inputs)];       /* The array to hold converted temps. */
char my_index = 0;                 /* Index into the two arrays.         */

int main(int argc, char **argv) {
    printf("The temperatures in Centigrade are:  ");
    printf("%d %d %d %d\n", inputs[0], inputs[1], inputs[2], inputs[3]);

    /* Fahrenheit = (9/5)Centigrade + 32 */

    printf("And their values in Fahrenheit are:  ");
    while (my_index < sizeof(inputs)) {
        outputs[my_index] = ((9/5) * inputs[my_index]) + 32;
        printf("%d ", outputs[my_index]);
        ++my_index;
    }
    printf("\n");
    return(0);
}
 