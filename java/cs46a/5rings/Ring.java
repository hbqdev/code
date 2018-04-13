import javax.swing.JComponent;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Ellipse2D;

/**
   A class that draw the Olympic rings.
*/
public class Ring
{
   /**
      Constructs a circle that represents the Olympic rings.
      @param anX the x coordinate
      @param aY the y coordinate
      @param aRadius the radius of the circle
      @param aColor the color of the ring
   */
   public Ring(int aX, int aY, int aRadius, Color someColor)
   {
       xLeft = aX;
       yTop = aY;
       radius = aRadius;
       aColor = someColor;  
         }

   /**
      Draws the ring.
      @param g2 the graphic context
   */
   public void draw(Graphics2D g2)
   {
      Ellipse2D.Double ring1  = new Ellipse2D.Double(xLeft+5,yTop+10,50,50);
      g2.setColor(aColor);
      g2.draw(ring1);
   }
private int xLeft;
private int yTop;
private int radius;
private Color aColor;

   
}