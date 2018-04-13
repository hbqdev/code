/**
 * Construct a Class that computes the volume and surface area of a Cylinder
 */
public class Cylinder
{
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
}
