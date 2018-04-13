import java.util.Scanner;
import java.util.Random;

public class Randomnumber2
{
    public static void main (String [] args)
    
   {
       int head = 0;
       int count = 0;
       Random r = new Random();
       Scanner sr  = new Scanner (System.in);
       System.out.println("Enter the number of trials");
       String number = sr.nextLine();
       double number2 = Double.parseDouble(number);
       for (int i = 1; i<=number2;i++)
        {
            head = 0;
            for (int j=1;j<=5;j++)
            {
                double p = r.nextDouble();
                if (p<0.5)
                head++;
            }
            if (head==3)
            {
                count++;
            }
            System.out.println("The probability is" + count/number2);
                
    }
}
}
    