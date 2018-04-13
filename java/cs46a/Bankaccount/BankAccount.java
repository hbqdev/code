/**
A bank account has a balance that can be changed by 
 deposits and withdrawals.
*/
public class BankAccount
 {  
 /**
 Constructs a bank account with a zero balance.
 */
 public BankAccount()
 {   
 balance = 0;
 }
 
  /**
 Constructs a bank account with a given balance.
 @param initialBalance the initial balance
 */
 public BankAccount(double initialBalance)
 {   
 balance = initialBalance;
 }
 
  /**
 Deposits money into the bank account.
 @param amount the amount to deposit
 */
public void deposit(double amount)
   {
      if (amount >=0)
      {
          double newBalance = balance + amount;
          balance = newBalance;
       }
       else
       {
           balance = balance;
       }
   }
 
  /**
  Withdraws money from the bank account.
  @param amount the amount to withdraw
 */
  public void withdraw(double amount)
   {
      if (amount > 0)
      {
          if ( balance - amount < 0)
          {
              balance = balance;
           }
           else
           {
               double newBalance = balance - amount;
               balance = newBalance;
                   }
       }
       else
       {
           balance = balance;
       }        
   }
 
 /**
 Gets the current balance of the bank account.
 @return the current balance
  */
 public double getBalance()
  {   
 return balance;
 }
 
private double balance;
}