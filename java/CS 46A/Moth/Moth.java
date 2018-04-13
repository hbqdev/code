/**
   This class models a moth flying across a straight line
*/
public class Moth
{
   /**
      Constructs a moth with a given position, facing right.
      @param initialPosition the initial position
   */
   public Moth(double initialPosition)
   {
      position = initialPosition;
      }
   
   /**
      Moves the moth halfway between the light position and the initial position.
   */
   public void moveToLight(double lightPosition)
   {
       direction = (lightPosition - position)/2.0;
      position = position + direction;
   }
   
   
   /**
      Gets the current position of this moth.
      @return the position
   */
   public double getPosition()
   {
      return position;
   }
   
   private double position;
   private double direction;
}
