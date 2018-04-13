import java.util.Arrays;

public class Words
{
   /**
      Removes all short words (length <= 3) from an array. The 
      order of the remaining element is left unchanged. The unused
      end of the array is filled with empty strings.
      @param words the array from which the short words are to be removed
   */
   public static void removeShortWords(String[] words)
   {
     for (int i=0; i<words.length;i++)
     {
         if ( words[i].length() <=3)
         {
             words[i] = words[i+1];
            }
        }



   }

   public static void main(String[] args)
   {
      String[] sentence = { "Mary", "had", "a", "little", "lamb" };
      removeShortWords(sentence);
      System.out.println(Arrays.toString(sentence));
   }
}
