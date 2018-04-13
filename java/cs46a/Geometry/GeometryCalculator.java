import java.util.Scanner;
public class GeometryCalculator
{
 public static void main (String[] args)
 {
  Scanner in = new Scanner(System.in);
  
  //reads number
  System.out.println("Please enter the radius: " );
  double radius = in.nextDouble();
  System.out.println("Please enter the height: ");
  double height = in.nextDouble();

System.out.println("The volume of the sphere is: "+Geometry.sphereVolume(radius));
System.out.println("The surface area of the sphere is: "+Geometry.sphereSurface(radius));
System.out.println("The volume of the cylinder is: " +Geometry.cylinderVolume(radius,height));
System.out.println("The surface area of the cylinder is: "+Geometry.cylinderSurface(radius,height));
System.out.println("The volume of the cone is: " +Geometry.coneVolume(radius,height));
System.out.println("The surface area of the cone is: "+Geometry.coneSurface(radius,height));
 }
 }

