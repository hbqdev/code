// TODO: Modify the constructor to throw an IllegalArgumentException
// if the initial balance or interest rate is < 0

/**
   An account that earns interest at a fixed rate.
*/
public class SavingsAccount extends BankAccount
{  
   /**
      Constructs a bank account with a given interest rate.
      @balance initialBalance the initial balance
      @param rate the interest rate
   */
   public SavingsAccount(double initialBalance, double rate) 
   {  
      super(initialBalance);
      interestRate = rate;
   }

   /**
      Adds the earned interest to the account balance.
   */
   public void addInterest() 
   {  
      double interest = getBalance() * interestRate / 100;
      deposit(interest); 
   }

   private double interestRate;

   // This method checks your work.
   
   public static String check(double initialBalance, double rate)
   {
      try
      {
         SavingsAccount account = new SavingsAccount(initialBalance, rate);
         return "constructed";
      }
      catch (IllegalArgumentException ex)
      {
         return "illegal argument";
      }
      catch (Exception ex)
      {
         return "another error";
      }
   }
}
