import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;

/**
 * Checks for collision
 * @author Jeremy Lozano
 */


public class CollisionDetector
{
    /**
     * Constructs a new Collision Detector
     */
    public CollisionDetector()
    {
    }

    /**
     * Checks whether the two rectangles intersect
     * @param one the first rectangle
     * @param two the second rectangle
     * @return whether the two rectangles intersect
     */
    public boolean checkCollision(Rectangle2D.Double one, Rectangle2D.Double two)
    {       
       return one.intersects(two);
    }
    
    /**
     * Checks whether the two rectangles intersect
     * @param one the first rectangle
     * @param two the second rectangle
     * @return whether the two rectangles intersect
     */
    public boolean checkCollision(Rectangle2D.Double one, Point2D.Double two)
    {       
       return one.contains(two.getX(), two.getY());
    }
}

