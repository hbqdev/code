import java.util.Scanner;
import java.lang.Math;
public class Distance2
{
   public static void main(String[] args)
   {
      Scanner in = new Scanner(System.in);

      System.out.print("Enter lat for the first point:");
      double lat1 = Math.toRadians(in.nextDouble());
      System.out.print("Enter longtitude  for the first point:");
      double long1= Math.toRadians( in.nextDouble());
      System.out.print("Enter lat for the second point:");
      double lat2 =  Math.toRadians(in.nextDouble());
      System.out.print("Enter longtitude for the second point:");
      double long2 = Math.toRadians( in.nextDouble());
      
     double distance = 3959*Math.acos(Math.sin(lat1)*Math.sin(long1)+Math.cos(lat2)*Math.cos(long2)*(long2-long1));

      System.out.println("The distance is " + distance);
   }
}
