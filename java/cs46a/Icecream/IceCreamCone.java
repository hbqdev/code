
/**
 A class that draw an icecream cone.
 */
public class IceCreamCone

{
/**
 Constructs an Icream Cone.
 */
   public IceCreamCone(double height, double radius)
   {
   someheight = height;
   someradius = radius;
   someside = Math.sqrt((someheight*someheight)+(someradius*someradius));
   SurfaceArea = Math.PI*someradius*someside;
   Volume = (1/3.0)*Math.PI*(someradius*someradius)*someheight;
}
public double getSurfaceArea()
{
  return SurfaceArea;
}
public double getVolume()
{
  return Volume;
}  
private double someheight;
private double someradius;
private double someside;
private double SurfaceArea;
private double Volume;
}

   