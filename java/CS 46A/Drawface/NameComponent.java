import javax.swing.JComponent;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
/**
   Draws a name in red inside a blue rectangle.
*/
public class NameComponent extends JComponent
{
   public void paintComponent(Graphics g)
   {
      Graphics2D g2 = (Graphics2D) g;
      Rectangle box = new Rectangle (5,5,200,50);
      g2.setColor(Color.BLUE);
      g2.fill(box);
      g2.setColor(Color.RED);
      g2.drawString("Tin Tran",15 , 20);
      
   }
}
