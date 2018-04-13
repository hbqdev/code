public class Sentence implements Measurable
{
   /**
      Constructs a sentence.
      @param text the text of the sentence. 
   */
   public Sentence(String text)
   {
      int n = text.length();
      String punctuation = text.substring(n - 1, n);
      words = text.substring(0, n - 1).split("\\s+");
   }
   
   /**
      Returns a word in this sentence.
      @param the index of the word 
      @return the ith word or an empty string if i is < 0
      or >= the number of words in this sentence
   */
   public String getWord(int i)
   {
      if (i >= 0 && i < words.length)
         return words[i];
      else
         return "";
   }
   
   public String toString()
   {
      String r = "";
      for (String w : words)
      {
         if (r.length() > 0) r += " ";
         r += w;
      }
      return r + punctuation;
   }

   // TODO: Do what it takes to implement the measurable interface
   // so that the measure of a sentence is the number of words.
   
   public double getMeasure()
   {
      return words.length;
    }

   private String[] words;
   private String punctuation;
}
