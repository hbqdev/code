import java.util.Scanner;
public class FactorPrinter
{
 public static void main (String[] args)
 {
  Scanner in = new Scanner(System.in);
  
  //reads number
  System.out.print("Enter a new integer: ");
  int factor = in.nextInt();
  
  //creates object
  FactorGenerator number = new FactorGenerator(factor);
  
  // prints the factors using the two methods
  while (number.hasMoreFactors())
  {
   System.out.println(number.nextFactor());
  }
 }
}