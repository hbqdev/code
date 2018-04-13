
/**
 * construct a class that count the total of 7 in any non positive integer.
 * 
 */
public class Numbers
{
   /**
   Counts the number digits with value 7 in a given number
   @param n any non-negative number
   @return the number digits with value 7 in the decimal representation of n
*/
public int countSevens(int n)
{
   while (n !=0)
   {
       if (n%10 ==7)
       count++;
       n = n/10;
             
    }
        return count;
}
    private int count;
}


