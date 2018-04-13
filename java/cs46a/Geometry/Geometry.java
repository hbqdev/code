
/**
 * Construct a class with methods that compute volumn and surface area of different objects
 */
public class Geometry
{
/**
  * compute the volume of a sphere
  */
 public static double sphereVolume(double r)
  {
 double volume = (4/3.0)*(Math.PI)*(r*r*r);
 return volume;
 }
   
 /**
      * compute the Surface area of a sphere
      */
 public static double sphereSurface(double r)
 {
   double SurfaceArea = 4.0*Math.PI*(r*r);
   return SurfaceArea;
}
/**
 * Computer the voume of a Cylinder
 */
public static double cylinderVolume(double r, double h)
{
double volume = Math.PI*(r*r)*h;
return volume;
}

/**
 * Compute the surface Area of a Cylinder
 */
public static double cylinderSurface(double r, double h)
{
double SurfaceArea = 2.0*Math.PI*(r*r) + 2.0*Math.PI*r*h;
return SurfaceArea;
}

/**
 * Compute the Volume of a cone
 */
public static double coneVolume(double r, double h)
{
double volume = (1/3.0)*Math.PI*(r*r)*h;
return volume;
}

/**
 * Compute the surface Area of a Cone
 */
public static double coneSurface(double r, double h)
{
double SurfaceArea = Math.PI*r*h + Math.PI*r*r;
return SurfaceArea;

}
    }