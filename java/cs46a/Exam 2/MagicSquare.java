/**
   A magic square that is constructed by a particular algorithm. 
*/
public class MagicSquare
{  
   /**
      Construct a MagicSquare object
      (precondition: s is odd).
      @param s the size of the square
   */
   public MagicSquare(int s)
   { 
      size = s;
      square = new int[size][size];

      for (int i = 0; i < size ; i++)
         for (int j = 0; j < size ; j++)
            square[i][j] = 0;

      int i = size - 1;
      int j = size / 2;

      for (int k = 0; k < size * size ; k++)
      {  
         /* [i][j] has been written already */
         if (square[i][j] != 0)
         {  
            if (j == 0 )
               j = size - 1;
            else
               j--;

            if (i == 0)
               i = size - 1;
            else
               i--; 
         }
         while (square[i][j] != 0)
         {  
            if (i == 0)
               i = size - 1;
            else
               i--;
         }

         square[i][j] = k + 1;
         i = (i + 1) % size;
         j = (j + 1) % size;
      }
   }

   /**
      Gets a string representation of the contents of this square.
      @return a string represenation of the square
   */
   public String toString()
   {        
      String r = "";
      for (int i = 0; i < size ; i++)
      {  
         for (int j = 0; j < size ; j++)
            r = r + String.format("%4d", square[i][j]);
         r = r + "\n";
      }
      return r;
   }

   private int[][] square;
   private int size;
}