
import java.awt.Graphics2D;
import java.awt.geom.Ellipse2D;
import org.alice.apis.moveandturn.Color;
import org.alice.apis.moveandturn.PointOfView;
import org.alice.apis.moveandturn.Position;
import org.alice.apis.moveandturn.Quaternion;
import org.alice.apis.moveandturn.gallery.shapes.Circle;

public class Beeper extends Circle {
    private int x;
    private int y;

    /**
     * Constructs a beeper at a given grid location.
     * @param x the x location of the beeper
     * @param y the y location of the beeper
     */
    public Beeper(int x, int y)
    {
        this.x = x;
        this.y = y;
        setColor(Color.RED);
        setWidth(0.25);
        setLocalPointOfView(new PointOfView(
                        new Quaternion(0, 0, 0, 1),
                        new Position(x, 0.1, y)));
    }
    
    /**
    * Gets the x location of the center of this beeper.
    * @return the x location
    */
    public int getX()
    {
        return x;
    }
    
    /**
    * Gets the y location of the center of this beeper.
    * @return the y location
    */
    public int getY()
    {
        return y;
    }

    /**
     * Draws this beeper in 2D. I use this for making diagrams.
     * @param g2 the graphics context
     */
    public void draw(Graphics2D g2)
    {
        final double RADIUS = 0.3;
        g2.draw(new Ellipse2D.Double(x - RADIUS, y - RADIUS, 2 * RADIUS, 2 * RADIUS));
    }
}
