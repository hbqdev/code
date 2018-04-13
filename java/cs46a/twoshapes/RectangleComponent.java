import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import javax.swing.JPanel;
import javax.swing.JComponent;
import java.awt.geom.Ellipse2D;

/**
   A component that draws two rectangles.
*/
public class RectangleComponent extends JComponent
{  
   public void paintComponent(Graphics g)
   {  
      // Recover Graphics2D
      Graphics2D g2 = (Graphics2D) g;

      // Construct a rectangle and draw it
      Ellipse2D.Double box =  new Ellipse2D.Double (35, 50, 30, 30);
      g2.draw(box);
      
      Ellipse2D.Double box2 =  new Ellipse2D.Double (20, 35, 60, 60);
      g2.draw(box2);
      // Move rectangle 15 units to the right and 25 units down
     //  box.translate(15, 25);

      // Draw moved rectangle
      g2.draw(box);
   }
}
