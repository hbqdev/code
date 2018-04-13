/**
 *
 * @author Tin Tran
 */

import java.io.*;
import java.util.*;

public class Quicksort{
    public static int Quicksort (int[] num, int p, int r)
    {
        int i=p,
        j=r, compare;
        int count=0;
        int x=num[(p+r)/2];
        while (num[i]<x)
        {
            i++;
            count++;
        }
        while (num[j]>x)
        {
            j--;
            count++;
        }
        if (i<=j)
        {
            compare=num[i];
            num[i]=num[j];
            num[j]=compare;
            i++;
            j--;
        }
    
    if (p<j)
        Quicksort(num, p, j);
    if (i<r)
        Quicksort(num, i, r);
   return count;
}


  public static void main(String args[]){
    int i;
    int num[] = {12,9,4,99,120,1,3,10};
   System.out.println("Before the sort:");
   for(i = 0; i < num.length; i++)
    {
    System.out.print( num[i]+"  ");
    }
    System.out.println();
    Quicksort(num,0,num.length-1);
    System.out.println("After the sort:");
    for(i = 0; i <num.length; i++)
    {
    System.out.print(num[i]+"  ");
    }
    System.out.println();
    System.out.println("The count is: "+ Quicksort(num,0,num.length-1));
    System.out.println();

  }

}
