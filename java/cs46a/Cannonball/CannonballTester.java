public class CannonballTester
{
   public static void main(String[] args)
   {
      Cannonball ball = new Cannonball(100, 45); // 100 m/sec
      ball.move(1); // move by one second

      double x = ball.getX();
      System.out.println(x);
      System.out.println("Expected: " + (100 * Math.sqrt(2) / 2));
      double y = ball.getY();
      System.out.println(y);
      System.out.println("Expected: " + (100 * Math.sqrt(2) / 2));
   }
}
