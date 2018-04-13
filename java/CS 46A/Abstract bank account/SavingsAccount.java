/**
  A savings account has a balance that can accrue interest on the minimum
 *balance amount.
  */
 public class SavingsAccount extends BankAccount
    {
      /**
      Constructs a new savings account with given bank account balance.
      @param rate the interest rate
       */
       public SavingsAccount(int rate)
        {
            iRate = rate;
       }
        
        /**
         Withdraws the given amount
         @param amount the amount withdrawn
        */
        public void withdraw(double amount)
        {
            super.withdraw(amount);
            minBalance = getBalance();
            
        }
    
        
        public void endOfMonth()
        {
            double interest = getBalance() * iRate / 100;
            deposit(interest); 
        }
        
        private int iRate;
        private double minBalance;
    
    
   }