
import java.awt.Graphics2D;
import java.awt.geom.Line2D;
import java.awt.geom.Point2D;
import org.alice.apis.moveandturn.gallery.scifi.KoalaRobot;
import org.alice.apis.moveandturn.*;

public class Robot extends KoalaRobot
{
    private int x;
    private int y;
    private int dx;
    private int dy;

    /**
     * Constructs a robot at a given grid location. The robot faces north.
     * @param x the x location of the robot
     * @param y the y location of the robot
     */
    public Robot(int x, int y)
    {
        this.x = x;
        this.y = y;
        setLocalPointOfView(new PointOfView(
            new Quaternion(0, 0, 0, 1),
            // new Quaternion(0, -Math.sqrt(0.5), 0, Math.sqrt(0.5)),
            new Position(x, -0.05, y)));
        dx = 0;
        dy = -1;
    }

    private AbstractCamera getCamera() {
        for (Composite match : getScene().findAllMatches()) {
            if (match instanceof AbstractCamera) {
                return (AbstractCamera) match;
            }
        }
        return null;
    }

    /**
     * Moves this robot in the direction into which it faces.
     */
    public void moveForward() {
        x += dx;
        y += dy;
        if (dy != 0)
        {
        final AbstractCamera camera = getCamera();
        DoTogether.invokeAndWait(
                new Runnable() {
                    public void run() {
                        move(MoveDirection.FORWARD, 1);
                    }
                },
                new Runnable() {
                    public void run() {
                        camera.move(dy == 1 ? MoveDirection.BACKWARD : MoveDirection.FORWARD, 1);
                    }
                });
        }
        else
            move(MoveDirection.FORWARD, 1);
    }

    /**
     * Turns this robot left.
     */
    public void turnLeft()
    {
        int newDx = dy;
        dy = -dx;
        dx = newDx;
        turn(TurnDirection.LEFT, 0.25);
    }

    /**
     * Turns this robot right.
     */
    public void turnRight()
    {
        int newDx = -dy;
        dy = dx;
        dx = newDx;
        turn(TurnDirection.RIGHT, 0.25);
    }

    /**
     * Checks whether there is a wall in front of this robot.
     * @return true if there is a wall, false otherwise.
     */
    public boolean frontHasWall()
    {
        for (Composite match : getScene().findAllMatches())
        {
            if (match instanceof Wall)
            {
                Wall w = (Wall) match;
                if (w.getX() == x + dx * 0.5 && w.getY() == y + dy * 0.5)
                    return true;
            }
        }
        return false;
    }

    /**
     * Checks whether there is a wall to the right of this robot.
     * @return true if there is a wall, false otherwise.
     */
    public boolean rightHasWall()
    {
        for (Composite match : getScene().findAllMatches())
        {
            if (match instanceof Wall)
            {
                Wall w = (Wall) match;
                if (w.getX() == x + -dy * 0.5 && w.getY() == y + dx * 0.5)
                    return true;
            }
        }
        return false;
    }

    /**
     * Checks whether there is a beeper under this robot.
     * @return true if there is a beeper, false otherwise.
     */
    public boolean isOverBeeper()
    {
        for (Composite match : getScene().findAllMatches()) {
            if (match instanceof Beeper) {
                Beeper b = (Beeper) match;
                if (b.getX() == x && b.getY() == y)
                    return true;
            }
        }
        return false;
    }

    public String toString()
    {
        return getClass().getName() + "[x=" + x + ",y=" + y + ",dx=" + dx + ",dy=" + dy + "]";
    }

    /**
     * Draws this robot in 2D. I use this for making diagrams.
     * @param g2 the graphics context
     */
    public void draw(Graphics2D g2)
    {
        Point2D.Double p1 = new Point2D.Double(x + 0.3 * dx, y + 0.3 * dy);
        Point2D.Double p2 = new Point2D.Double(x - 0.15 * dx, y - 0.15 * dy);
        Point2D.Double p3 = new Point2D.Double(x + 0.15 * dy - 0.3 * dx, y - 0.3 * dy + 0.15 * dx);
        Point2D.Double p4 = new Point2D.Double(x - 0.15 * dy - 0.3 * dx, y - 0.3 * dy - 0.15 * dx);
        g2.draw(new Line2D.Double(p1, p3));
        g2.draw(new Line2D.Double(p2, p3));
        g2.draw(new Line2D.Double(p1, p4));
        g2.draw(new Line2D.Double(p2, p4));
    }
}
