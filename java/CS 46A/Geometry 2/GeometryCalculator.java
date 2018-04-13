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

System.out.println("The volume of the sphere is: "+Sphere.sphereVolume(radius));
System.out.println("The surface area of the sphere is: "+Sphere.sphereSurface(radius));
System.out.println("The volume of the cylinder is: " +Cylinder.cylinderVolume(radius,height));
System.out.println("The surface area of the cylinder is: "+Cylinder.cylinderSurface(radius,height));
System.out.println("The volume of the cone is: " +Cone.coneVolume(radius,height));
System.out.println("The surface area of the cone is: "+Cone.coneSurface(radius,height));
 }
 }

