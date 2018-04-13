/**
 * Construct a class that computes the volume and surface area of a Cone
 */
public class Cone
{
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