/**
 * contructs a class that checks a string and returns the vowels within the string
 */
public class Words
{
/**
   Gets a string consisting of all vowels contained in a given string. Vowels are
   A E I O U a e i o u
   @param s a string
   @return a string with all vowels in s, in the order in which they appear in s
*/
public String getVowels(String s)
{
String letter = "";
for (int i=0; i<s.length();i++)
{ 
    if ("AEIOUaeiou".contains(s.substring(i,i+1)))
    {
    letter += s.substring(i,i+1);
    }
    }
    return letter;
}
}