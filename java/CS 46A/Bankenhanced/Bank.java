import java.util.ArrayList;

/**
   This bank contains a collection of bank accounts.
*/
public class Bank
{
   /**
      Constructs a bank with no bank accounts.
   */
   public Bank()
   {
      accounts = new ArrayList<BankAccount>();
   }
   
   /**
      Adds an account to this bank.
      @param a the account to add
   */
   public void addAccount(BankAccount a)
   {
      accounts.add(a);
   }
   
   /**
      Gets the sum of the balances of all accounts in this bank.
      @return the total balance
   */
   public double getTotalBalance()
   {
      double total = 0;
      for (BankAccount a : accounts)
      {
         total = total + a.getBalance();
      }
      return total;
   }
   
   /**
      Counts the number of bank accounts whose balance is at
      least a given value.
      @param atLeast the balance required to count an account
      @return the number of accounts having at least the given balance
   */
   public int count(double atLeast)
   {
      int matches = 0;
      for (BankAccount a : accounts)
      {
         if (a.getBalance() >= atLeast) matches++; // found a match
      }
      return matches;
   }

   /**
      Finds a bank account with a given number.
      @param accountNumber the number to find
      @return the account with the given number, or null if there
      is no such account
   */
   public BankAccount find(int accountNumber)
   {
      for (BankAccount a : accounts)
      {
         if (a.getAccountNumber() == accountNumber) // found a match
            return a;
      }
      return null; // no match in the entire array list
   }
   
   /**
      Gets the bank account with the largest balance.
      @return the account with the largest balance, or null if the
      bank has no accounts
   */
   public BankAccount getMaximum()
   {
      if (accounts.size() == 0) return null;
      BankAccount largestYet = accounts.get(0);
      
      for (int i = 1; i < accounts.size(); i++)
      {
         BankAccount a = accounts.get(i);
         if (a.getBalance() > largestYet.getBalance())
            largestYet = a;
      }
      return largestYet;
   }
   
   /**
      Adds an account to the bank.
      @param accountNumber the account number of this account
      @param initialBalance the initial balance of this account
   */
   public void addAccount(int accountNumber, double initialBalance)
   {
     accounts.add(new BankAccount(accountNumber, initialBalance));
     
   }
   
   /**
      Deposits money into an account
      @param accountNumber the account number
      @param amount the amount to be deposited
   */
   public void deposit(int accountNumber, double amount)
   {
      accounts.get(accountNumber);
      accounts.get(accountNumber).deposit(amount);
   }
   
   /**
      Withdraws money from an account.
      @param accountNumber the account number
      @param amount the amount to be withrawn
   */
   public void withdraw(int accountNumber, double amount)
   {
     accounts.get(accountNumber);
     accounts.get(accountNumber).withdraw(amount);
   }
   
   /**
      Gets an account balance
      @param accountNumber the account number
      @return the account balance
   */
   public double getBalance(int accountNumber)
   {
     accounts.get(accountNumber);
     return accounts.get(accountNumber).getBalance();
     
   }
   
   private ArrayList<BankAccount> accounts;
 
   
}