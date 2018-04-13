import java.awt.Graphics2D;
import java.awt.geom.Rectangle2D;
import org.alice.apis.moveandturn.Color;
import org.alice.apis.moveandturn.FillingStyle;
import org.alice.apis.moveandturn.PointOfView;
import org.alice.apis.moveandturn.Position;
import org.alice.apis.moveandturn.Quaternion;
import org.alice.apis.moveandturn.gallery.shapes.Square;

public class Wall extends Square
{
    public static final int X_DIRECTION = 1;
    public static final int Y_DIRECTION = 2;

    /**
     * Construct a wall that is north or west of a robot at a given location
     * @param x the x location of a robot adjacent to this wall
     * @param y the y location of a robot adjacent to this wall
     * @param direction X_DIRECTION or Y_DIRECTION
     */
    public Wall(int x, int y, int direction)
    {
        this.direction = direction;

        setHeight(2);
        setWidth(0.95);
        setColor(Color.PINK);

        Quaternion q;
        if (direction == X_DIRECTION)
        {
            this.x = x;
            this.y = y - 0.5;
            q = new Quaternion(0, 0, 0, 1);
        }
        else
        {
            this.x = x - 0.5;
            this.y = y;
            q = new Quaternion(0, Math.sqrt(0.5), 0, Math.sqrt(0.5));
        }
        setLocalPointOfView(new PointOfView(q, new Position(this.x, 0.5, this.y)));
    }

    /**
    * Gets the x location of the center of this wall.
    * @return the x location
    */
    public double getX()
    {
        return x;
    }

    /**
    * Gets the y location of the center of this wall.
    * @return the y location
    */
    public double getY()
    {
        return y;
    }

    /**
    * Gets the direction of this wall.
    * @return X_DIRECTION or Y_DIRECTION
    */
    public int getDirection()
    {
        return direction;
    }

    /**
     * Draws this beeper in 2D. I use this for making diagrams.
     * @param g2 the graphics context
     */
    public void draw(Graphics2D g2)
    {
        final double THICKNESS = 0.1;
        if (direction == X_DIRECTION)
            g2.fill(new Rectangle2D.Double(
                    x - 0.5 + THICKNESS / 2, y - THICKNESS / 2,
                    1 - THICKNESS, THICKNESS));
        else
            g2.fill(new Rectangle2D.Double(
                    x - THICKNESS / 2, y - 0.5 + THICKNESS / 2,
                    THICKNESS, 1 - THICKNESS));
    }


    private double x;
    private double y;
    private int direction;
}
