import java.awt.Shape;
import java.awt.geom.*;
import java.util.Random;

public class RandomShapeGenerator
{
public RandomShapeGenerator(int aWidth, int aHeight) 
{
width = aWidth;
height = aHeight;
}

public Shape randomShape()
{
Random r = new  Random();
int s = r.nextInt(3);
int x = r.nextInt(width);
int y = r.nextInt(height);
width1 = r.nextInt(100);
height1 = r.nextInt(150);
if (s == 0)
shape = new Rectangle2D.Double (x,y,width1,height1);
else if (s==1)
shape = new Line2D.Double(x,y,width1,height1);
else if (s==2)
shape  = new Ellipse2D.Double(x,y,width1,height1);
return shape;
}

private int width1;
private int height1;
private int width;
private int height;
private Shape shape;
}