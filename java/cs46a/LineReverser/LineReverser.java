import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;

public class LineReverser
{
   public static void main(String[] args)
      throws FileNotFoundException
   {
      String inputFileName = "mary.txt";
      String outputFileName = "output.txt";
      FileReader reader = new FileReader(inputFileName);
      Scanner fileIn = new Scanner(reader);
      PrintWriter out = new PrintWriter("output.txt");

      fileIn.close();
      out.close();
     out.println(fileIn.nextLine());
      
   }
}