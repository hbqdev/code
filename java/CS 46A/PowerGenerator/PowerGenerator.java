public class PowerGenerator
{
   /**
      Constructs a power generator.
      @param aFactor the number that will be multiplied by itself
   */
   public PowerGenerator(double aFactor) 
   { 
    factor = aFactor;   
    }

   /**
      Computes the next power.
   */
   public double nextPower() 
   { 
      power = Math.pow(factor, i);
      i++;
      return power;
    }
   private double power;
   private double factor;
   private double i;
}
 