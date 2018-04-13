 import java.util.Scanner;

 public class CurrencyConverter
 {
    public static void main(String[] args)
   {
     Scanner in = new Scanner(System.in);
     
      System.out.print("How many euros is one dollar?: ");
      double Exchangerate = in.nextDouble();
      boolean done = false;
      while (!done)
      {
         System.out.print("Dollar Value (Q to quit): ");
         String input = in.next();
         if (input.equalsIgnoreCase("Q"))
            done = true;
            
         else
         {
           double a = Double.parseDouble(input);
           double conversionrate = a*Exchangerate;
           System.out.printf("%.2f Dollar = %.2f", a, conversionrate);
    
        }
        
      }
     

     }
}
