public class Words
{
/**
     Gets the middle character or character pair from this word
     when possible.
     @param word a word
     @return the middle character (if the word length is odd) or
     middle two characters (if it is even), or the empty string if
     the word is empty, or null if it is null.
  */
  public String getMiddle(String word)
  {
    
if (word == null) return null;
if (word.equals("")) return "";
n = word.length();
i = n/2;

if (n%2==0)
{
middle = word.substring(i-1, i+1);
}
else if (n%2 !=0)
{
middle = word.substring(i,i+1);
    
  }
  return middle;
}
  private int n;
  private int i;
  private String middle;
}
