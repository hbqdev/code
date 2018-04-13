 /**
      This class generates all the factors of a number.
   */
   public class FactorGenerator
   {
      /**
         Creates a FactorGenerator object used to determine the factor of
         an input value.
         @param aNum is the input value
      */
      public FactorGenerator(int aNum)
      {
         number= aNum;
        }
      /**
         Determine whether or not there are more factors.
         @return true there are more factors

      */
      public boolean hasMoreFactors()
      {
        return (number>=lastFactor);
        }
        
      /**
         Calculate the next factor of a value.
         @return factor the next factor
      */
      public int nextFactor()
      {
          //if (!hasMoreFactors())
          //return -1;
          
          //int factor = lastFactor;
          
          //while(!((double)(number/factor) == ((double)number/(double)factor)))
          //{
            //  factor++;
            //}
            //number /= factor;
            //lastFactor = factor;
            //return lastFactor;
      int i =2;
      while (number %i!=0)
      i++;
      number /= i;
      return i;
    }
    private int number;
    private int lastFactor =2;
     
   } 