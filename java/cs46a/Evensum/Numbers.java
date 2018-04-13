public class Numbers
{
   /**
      Computes a sum of even integers 
      @param a the lower bound (may be odd or even)
      @param a the lower bound (may be odd or even)
      @return the sum of even integers between a and b (inclusive).
   */
   public int evenSum(int a, int b)
   {
     for (int x=a; x<=b; x++)
     {
     if (x%2==0)
     {
     sum = sum+x;
     }
     }
     return sum;
   }
   private int even;
   private int sum;
}
