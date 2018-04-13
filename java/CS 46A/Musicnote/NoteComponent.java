import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Line2D;
import javax.swing.JPanel;
import javax.swing.JComponent;
import java.awt.BasicStroke;

/**
   A component that draws a musical note.
*/
public class NoteComponent extends JComponent
{
   public void paintComponent(Graphics g)
   {
      // Recover Graphics2D
      Graphics2D g2 = (Graphics2D) g;

      // Construct and draw one note base
      Ellipse2D.Double base = new Ellipse2D.Double(10, 30, 10, 10);
      g2.fill(base);

      // Consruct and draw the stem
      Line2D.Double stem = new Line2D.Double(19, 10, 19, 35);
      g2.draw(stem);
      
        Line2D.Double stem3 = new Line2D.Double(40, 10, 40, 35);
      g2.draw(stem3);
      //Construc another note base
      Ellipse2D.Double base2 = new Ellipse2D.Double(30, 30, 10, 10);
      g2.fill(base2);
      
        g2.setStroke(new BasicStroke(5));
        Line2D.Double stem2 = new Line2D.Double(21, 10, 38.5, 10);
      g2.draw(stem2);
      
   }
}