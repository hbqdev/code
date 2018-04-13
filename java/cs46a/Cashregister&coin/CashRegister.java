/**
   *A cash register totals up sales and computes change due.
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
public void enterPayment(int coinCount, Coin CoinType)
{
coinnum = coinCount;
coin = CoinType;
Payment += coin.getValue()*coinnum;
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
private double Purchase;
private double Payment;
private double change;
private int coinnum;
private Coin coin;
public static final double QUARTER_VALUE = 0.25;
public static final double DIME_VALUE = 0.1;
public static final double NICKEL_VALUE = 0.05;
public static final double PENNY_VALUE = 0.01;
}
