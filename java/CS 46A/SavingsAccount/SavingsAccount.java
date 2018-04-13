public class SavingsAccount extends BankAccount
{
   public SavingsAccount(double rate)
   {
      interestRate = rate;
   }
   public void withdraw(double amount) 
   {  
      super.withdraw(amount);
      previousbalance = getBalance();
   }
      public void addInterest()
   {
      if ( previousbalance < getBalance())
      {
      minimumbalance = previousbalance;
      double interest = minimumbalance * interestRate / 100;
      deposit(interest);
    }
   }
   private double interestRate;
   private double minimumbalance;
   private double previousbalance;
}
