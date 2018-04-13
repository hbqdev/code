public class BankTester
{
   public static void main(String[] args)
   {
      Bank bank = new Bank();

      int dannysAccount = 0;
      int sallysAccount = 1;
      int harrysAccount = 2;
      int jerrysAccount = 3;
      
      bank.addAccount(dannysAccount, 1000);
      bank.addAccount(sallysAccount, 2000);
      bank.addAccount(harrysAccount, 3000);
      bank.addAccount(jerrysAccount, 10000);

      bank.deposit(dannysAccount, 200);
      bank.withdraw(sallysAccount, 500);
      bank.deposit(harrysAccount, 1000);
      bank.withdraw(jerrysAccount, 7000);

      System.out.println(
         "Danny's Account Balance: " + bank.getBalance(dannysAccount));
      System.out.println("Expected: 1200");
      System.out.println(
         "Sally's Account Balance: " + bank.getBalance(sallysAccount));
      System.out.println("Expected: 1500");
      System.out.println(
         "Harry's Account Balance: " + bank.getBalance(harrysAccount));
      System.out.println("Expected: 4000");
      System.out.println(
         "Jerry's Account Balance: " + bank.getBalance(jerrysAccount));
      System.out.println("Expected: 3000");
   }
}