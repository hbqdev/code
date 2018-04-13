import javax.swing.JComponent;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;

public class TwoSquareComponent extends JComponent
{
   public void paintComponent(Graphics g)
   {
      Graphics2D g2 = (Graphics2D) g;
      Rectangle box = new Rectangle (5,10,50,50);
     g2.setColor(Color.PINK);
     g2.fill(box);
     Color magenta = new Color(128,0,128);
     Rectangle box2 = new Rectangle(5,50,50,50);
     g2.setColor(Color.magenta);
     g2.fill(box2);
   }
}
