import java.awt.geom.Point2D;
import java.awt.Graphics2D;
import java.util.ArrayList;
import java.awt.geom.Line2D;
/**
 * construc a class that draws a polygon by connecting points.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Polygon
{
public Polygon()
{
poly = new ArrayList<Point2D.Double>();
  }

  public void add(Point2D.Double aPoint)
{
poly.add(aPoint);
}
public void draw(Graphics2D g2)
{
//for (int i =0; i<poly.size();i++)
//{
//if (i == poly.size()-1)
//{/
//Point2D.Double from = poly.get(i);/
//Point2D.Double to = poly.get(0);
//Line2D.Double linef = new Line2D.Double (from, to);
//g2.draw(linef);
//}
//else 
//{
//Point2D.Double from = poly.get(i);
//Point2D.Double to = poly.get(i+1);
//Line2D.Double lines = new Line2D.Double(from, to);
//g2.draw(lines);
Point2D.Double previousPoint = poly.get(poly.size()-1);
for (Point2D.Double point : poly)
{
Line2D.Double line = new Line2D.Double(point, previousPoint);
g2.draw(line);
previousPoint = point;
}
}
private ArrayList<Point2D.Double> poly;
 } 