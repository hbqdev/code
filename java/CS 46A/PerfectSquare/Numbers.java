public class Numbers
{
   /**
      Computes a sum of Perfec Squares integers 
      @param a the lower bound (may be odd or even)
      @param a the lower bound (may be odd or even)
      @return the sum of perfectt integers between a and b (inclusive).
   */
   public int countPerfectSquares(int a, int b)
   {
     for (int x=a; x<=b; x++)
     {
     if (Math.sqrt(x)%1 ==0)
     {
     count++;
     }
     }
     return count;
   }
   private int count;
}
