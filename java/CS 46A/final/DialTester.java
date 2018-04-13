public class DialTester
{
   public static void main(String[] args)
   {
      Dial lock = new Dial();
      lock.turnLeft();
      lock.turnLeft();
      System.out.println(lock.currentNumber());
      System.out.println("Expected: 2");
      lock.turnRight();
      lock.turnRight();
      lock.turnRight();
      System.out.println(lock.currentNumber());
      System.out.println("Expected: 39");
   }
}