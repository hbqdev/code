/**
   Tests the bank account class with interest.
*/
public class BankAccountTester
{
   public static void main(String[] args)
  {
       BankAccount momsSavings = new BankAccount(1000);
       momsSavings.addInterest(10);
       System.out.println(1100);
       System.out.println("Expected:1100");
   }
}
