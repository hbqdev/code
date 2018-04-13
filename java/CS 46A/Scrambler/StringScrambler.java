public class StringScrambler
{
   public String scramble(String word)
   {
       String first, second, third, SwapOne, SwapTwo;
       String middle;
       String last;
       int i = randomInt(0,word.length()-1);
       
        first = word.substring(0,i);
        SwapOne = word.substring (i,i+1);
        SwapTwo = word.substring(i+1,i+2);
        last = word.substring (i+2, word.length());
         word = first+SwapTwo+SwapOne+last ;
      return word;
   }

   /**
      Returns a random integer between begin and pastEnd - 1
      @param begin the lower bound (inclusive)
      @param end the upper bound (exclusive)
   */
   public int randomInt(int begin, int pastEnd)
   {
      return (int)((pastEnd - begin) * Math.random());
   }

   /**
      Scrambles all words of length > 3 in a given sentence, after stripping off 
      white space and punctuation marks (except for '). Do not look inside this
      method. If you do, be sure to avert your eyes from the split method call, or permanent eye damage may occur.
      @param sentence a string consisting of one or more words
      @return the string witht the words scrambled
   */
   public String scrambleSentence(String sentence)
   {
      String result = "";
      for (String w : sentence.split("[\\s\\p{Punct}&&[^']]+"))
      {
         String r;
         if (w.length() > 3) r = scramble(w);
         else r = w;
         result = result + r + " ";
      }

      return result;
   }

}
