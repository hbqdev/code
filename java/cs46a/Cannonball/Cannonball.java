/**
   This class simulates a cannonball fired at an angle.
*/
public class Cannonball
{
   /**
      Constructs a Cannonball.
      @param ivel the initial velocity of the ball
      @param angle the angle at which the cannonball was launched
      (in degrees)
   */
   public Cannonball(double ivel, double angle) 
   { 
       vel0 = vel = ivel;
       angle0 = angle*Math.PI/180.0;
      }

   /**
      Updates the position and velocity of this cannonball 
      after a given time interval.
      @param deltaT the time interval
   */
   public void move(double deltaT) 
   {
      t= deltaT;
      x += vel0*(Math.cos(angle0))*t;
      y += vel * Math.sin(angle0)*t; 
      vel = vel - (g * t); 
      }

   /**
      Gets the x position of this cannonball.
      @return the horizontal position
   */
   public double getX() 
   { 
      return x;
       }

   /**
      Gets the y position of this cannonball.
      @return the vertical position
   */
   public double getY() 
   { 
      return y;
       }
  private double vel0;
  private double angle0;
  private double vel;
  private double x;
  private double y;
  private double t;
  private static final double g = 9.81;
}
