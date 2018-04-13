import java.util.ArrayList;

public class WordUtil2
{
   /**
      Returns the character that forms the longest repetition in this string. 
      @param str a string of length > 0
      @return the character occurring in the longest most repetition in str. If more than one letter occur with the 
      same maximum length, return any one of them.
   */
   public static char longestRepeated(String str)
     {
       
       for(int i = 0; i<str.length()-1;i++)
        if (str.charAt(i) == str.charAt(i+1))
          {
              ch = str.charAt(i);
              
          }
return ch;
              
        }
           
   public static void main(String[] args)
   {
      char c1 = longestRepeated("Hello");
      System.out.println(c1);
      System.out.println("Expected: l");
      char c2 = longestRepeated("Hellooo!!!");
      System.out.println(c2);
      System.out.println("Expected: o or !");
   }
   
   private static char ch;
  }
