import javax.swing.JComponent;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Ellipse2D;

public class EllipseComponent extends JComponent
{
   public void paintComponent(Graphics g)
   {
      Graphics2D g2 = (Graphics2D) g;
    Ellipse2D.Double ellipse  = new Ellipse2D.Double(0, 0, 282, 362);
      g2.setColor(Color.RED);
      g2.fill(ellipse);
   }
}
