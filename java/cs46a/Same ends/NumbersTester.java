public class NumbersTester
{
 public static void main(String[] args)
 {
      int[] values1 = {1,4,5,1,1,4,1,5};
      System.out.println("EndCount = " + Numbers.sameEnds(values1));
      System.out.println("Expected = 0");
      int[] values2 = {1,4,2,7,5,1,6,1,4};
      System.out.println("EndCount = " + Numbers.sameEnds(values2));
      System.out.println("Expected = 2");
      int[] values3 = {1,4,2,7,5,1,4,1,4};
      System.out.println("EndCount = " + Numbers.sameEnds(values3));
      System.out.println("Expected = 2");
      int[] values4 = {1,4,4,2,5,1,4,4,1,4};
      System.out.println("EndCount = " + Numbers.sameEnds(values4));
      System.out.println("Expected = 2");
 }
}