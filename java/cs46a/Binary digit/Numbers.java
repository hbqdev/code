public class Numbers
{
   /**
      Returns the number of digits in the binary
      representation of a number
      @param n a nonnegative number
      @return the number of binary digits needed to
      represent n
   */
   
 public static int binaryDigits(int aNumber)
 {
    int count = 1;
    if (aNumber/2 ==0)
    return count;
    while (aNumber/2 !=0)
    {
    aNumber = aNumber/2;
    count++;
     }
     return count;
}
   
   public static void main(String[] args)
   {
      System.out.println(binaryDigits(20));
   }
}