/* 
 * File:   main.c
 * Author: hanbaoquan
 *
 * Created on October 26, 2010, 11:16 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

#define BLOCK_SIZE 10
#include "ia.h"
/* get common definitions */
#define ia_init(array_ptr)
{
    (array_ptr)->next = NULL;
}
int index;
int num;
int status;

int num_step;
int main()
{
    for(index =1;index<num;index++)
    {
        status=ia_locate(index)->data[index%BLOCK_SIZE][0];
        num_step = ia_locate(index)->data[index%BLOCK_SIZE][1];
                switch(status)
        {
                    case 0: {} break;
                    case -1: {} break;
                    case -3: {} break;
                    default: {} break;

        }
    }
    return(0);
}
extern int ia_get(struct infinite_array *array_ptr, int index);

struct infinite_array {
/* the data for this block */
float
data[BLOCK_SIZE];
/* pointer to the next array */
struct infinite_array *next;
};

struct infinite_array *ia_locate(
struct infinite_array *array_ptr, int index,
int *current_index_ptr)
{
/* pointer to the current bucket */
struct infinite_array *current_ptr;
current_ptr = array_ptr;
*current_index_ptr = index;
while (*current_index_ptr >= BLOCK_SIZE) {
if (current_ptr->next == NULL) {
current_ptr->next = malloc(sizeof(struct infinite_array));
if (current_ptr->next == NULL) {
fprintf(stderr, "Error:Out of memory\n");
exit(8);
}
memset(current_ptr->next, '\0', sizeof(struct
infinite_array));
}
current_ptr = current_ptr->next;
*current_index_ptr -= BLOCK_SIZE;
}
return (current_ptr);
}

void
ia_store(struct infinite_array * array_ptr,
int index, int store_data)
{
/* pointer to the current bucket */
struct infinite_array *current_ptr;
int
current_index;
/* index into the current bucket */

current_ptr = ia_locate(array_ptr, index, &current_index);
current_ptr->data[current_index] = store_data;
}

int ia_get(struct infinite_array *array_ptr, int index)
{
/* pointer to the current bucket */
struct infinite_array *current_ptr;
int
current_index;
/* index into the current bucket */
current_ptr = ia_locate(array_ptr, index, &current_index);
return (current_ptr->data[current_index]);
}
