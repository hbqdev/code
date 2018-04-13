public class Strings
{
   /**
      Gets the last n characters from a string.
      @param s a string
      @param n a nonnegative integer <= s.length()
      @return the string that contains the last n characters of s
   */
   public String last(String s, int n)
   {
   stringlength = s.length();
   String last= s.substring(stringlength-n);
   return last;
   
   }
   
private int stringlength;
}
