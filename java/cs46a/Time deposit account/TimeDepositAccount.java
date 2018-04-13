public class TimeDepositAccount extends BankAccount
{
public TimeDepositAccount (int rate, int months)
{
interestRate = rate;
month = months;
}
public int getMounth()
{
return month;
}
public void withdraw(double amount)
{
if  (month >0)
super.withdraw(20);
super.withdraw(amount);
}

public void addInterest() 
   { 
       month--;
         double interest = getBalance() * interestRate / 100;
      deposit(interest); 
    
   }

private int interestRate;
private int month;
private double newbalance;
}