
/**
 * Write a description of class FairCoin here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
import java.util.Random;
import java.util.Scanner;
public class RandomNumber
{
   public static void main (String [] args)
   {
   Random r = new Random();
   Scanner sr = new Scanner (System.in);
   System.out.println("Enter the number of trial");
   String number = sr.nextLine();
   double number2 = Double.parseDouble(number);
      int counter = 0;
   for(int i=1;i<=number2;i++)
      {
          double p = r.nextDouble();
          System.out.println(" " + p);
          if (0<=p && p<=0.5)
          {
              counter++;
              }
        }
          System.out.println("Probability of head" +" "+ counter/number2);
         }
       
       

    
}