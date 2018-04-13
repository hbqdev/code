import java.util.Arrays;

public class ArrayUtil1
{
   /**
      Puts all zeroes in the array to the front. The order of the other elements may be changed.
      @param values an array of integers
   */
   public static void putAllZeroesToFront(int[] values)
   {
       int [] temp = values;

      for (int i=1; i<values.length;i++)
       {
             if(values[i] != 0)
             {
              for (int k=temp.length-1;k>0;k--)
             temp[k]=values[i];
                values=temp;
            }
          
}
}


   public static void main(String[] args)
   {
      int[] test1 = new int[] {0, 1, 4, 0, 9, 0, 16, 0, 25};
      putAllZeroesToFront(test1);
      System.out.println(Arrays.toString(test1));
      System.out.println("Expected: [0, 0, 0, 0, followed by a permutation of 1, 4, 9, 16, 25]");
   }
}
