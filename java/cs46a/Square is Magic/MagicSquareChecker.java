import java.util.ArrayList;
import java.util.Scanner;

/**
   This class tests whether a sequence of inputs forms a magic square.
*/
public class MagicSquareChecker
{
private ArrayList<Integer> numbers;
   public static void main(String[] args)
   {
      ArrayList<Integer> numbers = new ArrayList<Integer>();
      Scanner in = new Scanner(System.in);
      boolean more = true;

      System.out.println("Enter a sequence of integers, followed by Q: ");
      while (in.hasNextInt())
      {
         numbers.add(in.nextInt());
      }

      int size = (int) Math.ceil (Math.sqrt(numbers.size()));
      int k = 0;
      for (int i = 0; i < size ; i++)
      {
         for (int j = 0; j < size ; j++)
                    {
                      if (k < numbers.size())
                      {
                         System.out.printf("%4d", numbers.get(k));
                         k++;
                      }
         }
      }
      
      System.out.println();
   
   
    


   
   if (size*size == numbers.size())
   {
      Square mySquare = new Square(numbers);
      if(mySquare.isMagic())
          System.out.println("It's a magic square.");
                    else
                      System.out.println("It's not a magic square.");
      }
      else
          System.out.println("It's not a square.");
   }
}



