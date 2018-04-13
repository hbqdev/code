public class Numbers
{
   /**
      Computes the number of even and odd values in a given array
      @param values an array of integer values
      @return an array of length 2 whose 0 entry contains the count
      of even elements and whose 1 entry contains the count of odd
      values
   */
   public int[] evenOdds(int[] values)
   {
       int [] eveno = new int [2];
        evens=0;
        odds =0;
   for (int i =0; i<values.length;i++)
   {
      
        if (values [i] %2==0)
        evens++;
        else if (values [i] %2!=0)
        odds++;
            }
       eveno [0] = evens;
        eveno [1] = odds;  
        return eveno;
 }
 private int evens;
 private int odds;
 
}
