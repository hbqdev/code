import javax.swing.JComponent;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Line2D;
import javax.swing.JPanel;
import javax.swing.JComponent;


/**
   Draws a face.
*/
public class FaceComponent extends JComponent
{
   public void paintComponent(Graphics g)
   {
      Graphics2D g2 = (Graphics2D) g;
      Ellipse2D.Double head = new Ellipse2D.Double(5, 10, 200, 200);
      g2.draw(head);
       Ellipse2D.Double eye1 = new Ellipse2D.Double(35, 40, 30, 30);
       g2.draw(eye1);
         Ellipse2D.Double eye2 = new Ellipse2D.Double(140, 40, 30, 30);
       g2.draw(eye2);
       Line2D.Double mouth = new Line2D.Double(55, 150, 145, 150);
       g2.draw(mouth);
   }
}
