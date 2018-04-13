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
  Purchase +=amount;
}
public void enterPayment(double amount)
{
Payment += amount;
}
/**
   Computes the change due and resets the machine for the next customer.
   @return the change due to the customer
*/
public int giveChange(Coin coinType)
{
 change1 = Payment - Purchase;
 Purchase =0;
 int numberCoins = (int) (change1/coinType.getValue());
 change1 -= numberCoins*coinType.getValue();
 return numberCoins;
 
}
private double Purchase;
private double Payment;
private double change;
private double change1;
private double anamount;
private Coin coin;

}
