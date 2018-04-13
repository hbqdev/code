/**
 * Contrucs a class that calculates the volume and the Surface area of a Sphere
 */
public class Sphere
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
}