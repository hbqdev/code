public class Word
{
   /**
      Tests whether a letter is a vowel
      @param letter a string of length 1
      @return true if letter is a vowel
    */
   public boolean isVowel(String letter)
   {
       if (letter.equals("a") || letter.equals("A") || letter.equals("e") || letter.equals("E") || letter.equals("i") || letter.equals("I") || letter.equals("o") || letter.equals("O") || letter.equals("u") || letter.equals("U")) return true;
   else
   {
       return false;
    }
   }
}