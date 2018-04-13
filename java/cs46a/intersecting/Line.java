public class Line
{
   /**
      Construct a line with equation y = mx + b
      @param aSlope the slope of this line
      @param aYIntercept the y intercept of this line
   */
   public Line(double aSlope, double aYIntercept)
   {
      slope = aSlope;
      yIntercept = aYIntercept;
   }

   /**
      Checks whether a point is contained on the line
      @param x the x-coordinate of the point
      @param y the y-coordinate of the point
      @return true if (x,y) is contained in the line
   */
   public boolean contains(double x, double y)
   {      
      return Math.abs(x * slope + yIntercept - y) < EPSILON;
   }

   /**
      Gets the slope of this line
      @return the slope
   */
   public double getSlope()
   {
      return slope;
   }

   /**
      Gets the y intercept of this line
      @return the y intercept
   */
   public double getYIntercept()
   {
      return yIntercept;
   }

   /**
      Checks whether this line intersects with another.
      @param other another line
      @return true if this line and other intersect
   */
   public boolean intersects(Line other)
   {
    if (slope!=other.slope)
    {
        return true;
    }
    else if (yIntercept == other.yIntercept)
    {
        return true;
    }
    else
    {
        return false;

  }
}
   private double slope;
   private double yIntercept;

   private static final double EPSILON = 1E-12;

   // this method is used to check your work

   public static boolean check(double slope1, double yIntercept1,
      double slope2, double yIntercept2)
   {
      Line first = new Line(slope1, yIntercept1);
      Line second = new Line(slope2, yIntercept2);
      return first.intersects(second);
   }
}
