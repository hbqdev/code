/**
   A cash register totals up sales and computes change due.
*/
public class CashRegister
{
   /**
      Constructs a cash register with no money in it.
   */
   public CashRegister()
   {
      Purchase = 0;
      Payment = 0;
   }
/**
   Records the sale of an item.
   @param amount the price of the item
*/
public void recordPurchase(double amount)
{
   double newTotal = Purchase + amount;
   Purchase = newTotal;
}

/**
   Computes the change due and resets the machine for the next customer.
   @return the change due to the customer
*/
public double giveChange()
{
   change = Payment - Purchase;
   Purchase = 0;
   Payment = 0;
   return change;
}
public void enterPayment(int amount, int amount2, int amount3, int amount4, int amount5)
{
int Payment = amount;
}
public int giveDollars()
{
dollars =(int)(change);
change-= dollars;
return dollars;
}
public int giveQuarters()
{
int quarters =(int) ((change)/0.25);
change -=quarters;
return quarters;
}
public int giveDimes()
{
dimes = (int) (change/0.1);
change -=dimes;
return dimes;
}
public int giveNickels()
{
nickels= (int) (change/0.05);
change -=nickels;
return nickels;
}
public int givePennies()
{
pennies= (int) (change/0.01);
return pennies;
}
private double Purchase;
private double Payment;
private int pennies;
private int nickels;
private int dimes;
private int quarters;
private int dollars;
private double change;

public static final double QUARTER_VALUE = 0.25;
public static final double DIME_VALUE = 0.1;
public static final double NICKEL_VALUE = 0.05;
public static final double PENNY_VALUE = 0.01;
}
