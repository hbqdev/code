public class Word
{
   private String text;

   /**
      Constructs a word.
      @param text the characters in this word
   */
   public Word(String text)
   {
      this.text = text;
   }

   /**
      Tests whether a letter is a vowel
      @param letter a string of length 1
      @return true if letter is a vowel
    */
   public boolean isVowel(String letter)
   {
      return "aeiouy".contains(letter.toLowerCase());
   }

   public int countVowels()
   {
      int i = 0;
      int counter = 0;
      while (i < text.length())
      {
         String letter = text.substring(i, i + 1); // the ith letter
         if( isVowel(letter))
         counter++;
         i++;

      }
      return counter;
   }
  

   public int countVowelGroups()
   {
      int i = 0;
      int counter = 0;
      int foundvowel = 0;
      while (i <text.length())
      {
          String letter = text.substring(i, i+1);
          if( isVowel(letter))
          foundvowel = 1;
          else if (foundvowel==1)
          { 
              counter++; foundvowel =0;
   }
   else if (i==0 && !isVowel(letter))
   {
       counter++;
    }
    i++;
}
return counter;
}
   
   public String toString()
   {
      return text;
   }
   
}
