import javax.swing.JComponent;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Ellipse2D;

/**
   Draws the trajectory of a cannonball.
*/
public class CannonballComponent extends JComponent
{
   /**
      Constructs a component that paints the flight of a cannonball 
      @param ivel the initial velocity of the ball
      @param ang the angle at which the cannonball was launched
   */
   public CannonballComponent(double ivel, double ang)
   {
      vel0 =ivel;
      angle0=ang;
    
      
   }

   public void paintComponent(Graphics g)
   {
      Graphics2D g2 = (Graphics2D) g;
      ball = new Cannonball(vel0, angle0);
      while(ball.getY() >= 0)
      {
         ball.move(DELTA_T);
      Ellipse2D.Double circle = new Ellipse2D.Double(ball.getX(),getHeight()-ball.getY(), 4,4);
      g2.draw(circle);
      g2.setColor(Colors.BLUE);
      g2.fill(circle);
      }
   }

   private Cannonball ball;
   private double vel0;
   private double angle0;
   private static final double DELTA_T = 0.1;
}
