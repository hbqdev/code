import javax.swing.JComponent;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Ellipse2D;
import java.awt.BasicStroke;

/**
   Draws the olympic rings.
 */
public class OlympicRingComponent extends JComponent
{
   public void paintComponent(Graphics g)
   {
            
      Graphics2D g2 = (Graphics2D) g;
      g2.setStroke(new BasicStroke(4));
      Ring ring1 = new Ring(0,0,50,Color.BLUE);
      ring1.draw(g2);
      Ring ring2 = new Ring(50,0,50,Color.BLACK);
      ring2.draw(g2);
      Ring ring3 = new Ring(100,0,50,Color.RED);
      ring3.draw(g2);
      Ring ring4 = new Ring(25,25,50,Color.YELLOW);
      ring4.draw(g2);
      Ring ring5 = new Ring(75,25,50,Color.GREEN);
      ring5.draw(g2);
      // construct and draw five Ring objects
   }
}
