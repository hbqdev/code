/**
   This program tests the CashRegister class.
*/
public class CashRegisterTester
{
   public static void main(String[] args)
   {
      final double PENNY_VALUE = 0.01;
      final double NICKEL_VALUE = 0.05;
      final double DIME_VALUE = 0.1;
      final double QUARTER_VALUE = 0.25;

      CashRegister myRegister = new CashRegister();
      myRegister.recordPurchase(0.82);
      myRegister.enterPayment(1.00);

      Coin[] CoinTypes = new Coin[]
      {
         new Coin(QUARTER_VALUE, "quarter"),
         new Coin(DIME_VALUE, "dime"),
         new Coin(NICKEL_VALUE, "nickel"),
         new Coin(PENNY_VALUE, "penny")
      };
      int[] expected = { 0, 1, 1, 3 };
   
      for (int i = 0; i < CoinTypes.length; i++)
      {
         Coin c = CoinTypes[i];
         int change = myRegister.giveChange(c);
         System.out.println(c.getName() + ": " + change);
         System.out.println("Expected: " + expected[i]);
      }
   }
}
