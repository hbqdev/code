/**
   A simulated cash register that tracks the item count and
   the total amount due.
 */
public class CashRegister
{
   private int itemCount;
   private double totalPrice;

   /**
      Constructs a cash register with cleared item count and total.
   */
   public CashRegister()
   {
      itemCount = 0;
      totalPrice = 0;
   }

   /**
      Adds an item to this cash register.
      @param price the price of this item
   */
   public void addItem(double price)
   {
      itemCount++;
      totalPrice = totalPrice + price;
   }

   /**
      Gets the price of all items in the current sale.
      @return the total amount
   */
   public double getTotal()
   {
      return totalPrice; 
   }
   
   /**
      Gets the number of items in the current sale.
      @return the item count
   */
   public int getCount()
   {
      return itemCount; 
   }

   /**
      Gives change, clears the item count and the total.
      @param payment the payment given by the customer
   */
   public double giveChange(double payment)
   {
      double change = payment - totalPrice;
      itemCount = 0;
      totalPrice = 0;
      return change;
   }
}


