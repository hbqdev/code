import static java.lang.Math.PI;
import java.util.Random;

/**
   Normalizes an angle.
   @param angle an integer angle (may be negative)
   @return the equivalent angle in the range 0 ... 359
*/
public class Angle
{
public double normalize(int angle)
{
 anangle = angle;
return (anangle %= 4*PI);
}
private double anangle;
       
      
      
}

