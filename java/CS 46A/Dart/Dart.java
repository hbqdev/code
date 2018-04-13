import java.util.Random;
public class Dart
{
   Random generator = new Random();
   public Dart() 
   { 
       hits=0;
       tries=0;
    }

   /**
      Throws a dart into the square [-1,1] x [1,1] and records
      whether it hits the unit circle.
   */
   public void throwIntoSquare() 
   {
    double x = generator.nextDouble()*2-1;
    double y = generator.nextDouble()*2-1;
    tries++;
    if ((y<=Math.sqrt(1-x*x))&& y>=0)
    hits++;
    else if ((y>=Math.sqrt(1-x*x))&& y<=0)
    hits++;
   
}
    
     /**
      Gets the number of hits inside the unit circle.
      @return hits number of hits
   */
   public int getHits() 
   {
       return hits;
    }

   /**
      Gets the number of tries.
      @return the number of times the dart was thrown
   */
   public int getTries() 
   {
       return tries;
      }

   // private implementation 
   private int hits;
   private int tries;
}
 

