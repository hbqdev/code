public class CashRegisterTester
{
   public static void main(String[] args)
   {
      CashRegister reg = new CashRegister();
      reg.addItem(1);
       reg.addItem(1);
        reg.addItem(1);
      reg.getTotal();
       System.out.println("Items: " + reg.getCount());
      System.out.println("Expected: 3");
       System.out.println("Change: " + reg.giveChange(3.5));
      System.out.println("Expected: 0.50");
   }
}
