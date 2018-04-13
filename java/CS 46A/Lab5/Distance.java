import java.util.Scanner;

public class Distance
{
   public static void main(String[] args)
   {
      Scanner in = new Scanner(System.in);

      System.out.print("Enter x for the first point:");
      double x1 = in.nextDouble();
      System.out.print("Enter y  for the first point:");
      double y1 = in.nextDouble();
      System.out.print("Enter x for the second point:");
      double x2 = in.nextDouble();
      System.out.print("Enter y for the second point:");
      double y2 = in.nextDouble();

      double dx = x2-x1;
      double dy =y2-y1;
      double distance = Math.sqrt(dx*dx+dy*dy);

      System.out.println("The distance is " + distance);
   }
}
