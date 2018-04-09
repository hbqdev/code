/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package assignment2;
import java.util.*;
/**
 *
 * @author Han Bao Quan
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args)
    {
       System.out.println("Please enter number here: ");
       Scanner num = new Scanner(System.in);
       int number = Integer.parseInt(num.nextLine());
       if(isPerfect(number)==1)
       {
           System.out.println(number +" " + "is perfect");
       }
 else if (isPerfect(number)==0)
       {
     System.out.println("Number is not perfect");
 }
       
    }
public static int isPerfect(int num)
    {
    int sum=0;
    for (int i=1;i<num;i++)
    {
        int c = num%i;
        if(c==0)
        {
            sum=sum+i;
        }
    }
    if(sum==num)
    return 1;
    else
        return 0;
}
}
