import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;


/**
   A class to count the number of characters, words, and lines in files.
*/
public class FileCounter
{
   /**
      Constructs a FileCounter object.
   */
   public FileCounter()
   {
 
   }

   /**
      Processes an input source and adds its character, word, and line
      counts to this counter.
      @param in the scanner to process
   */
   public void read(Scanner in)
   {
       in1 = in;
      count1 = 0;
      character1=0;
       while (in1.hasNext())
       {
       String line = in1.nextLine();
       Scanner in2 = new Scanner(line);
       if(in2.hasNext())
       {
           String word = in2.next();
       count1++;
    }
       line1++;
       character1+=line.length();        
    }
   }

   /**
      Gets the number of words in this counter.
      @return the number of words
   */
   public int getWordCount()
   {
        
         return count1;
   }

   /**
      Gets the number of lines in this counter.
      @return the number of lines
   */
   public int getLineCount()
   {
      return line1;
    }
   /**
      Gets the number of characters in this counter.
      @return the number of characters
   */
   public int getCharacterCount()
   {
      return character1;
   }
private FileCounter counter;
private Scanner in1;
private int count1;
private int line1;
private int character1;

}
