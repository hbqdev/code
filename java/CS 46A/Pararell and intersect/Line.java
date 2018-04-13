public class Line
{
   /**
      Construct a line with equation y = mx + b
      @param aSlope the slope of this line
      @param aYIntercept the y intercept of this line
   */

   public Line(double x, double y, double aslope)
   {
      pointx = x;
      pointy=y;
      slope = aslope;
     }
  public Line (double x1, double y1, double x2, double y2)
  {
      pointx1 = x1;
      pointx2 = x2;
      pointy1 = y1;
      pointy2 = y2;
      slope = ((y2-y1)/(x2-x1));
      yIntercept = y2-slope*x2;
    }
    public Line(double aslope, double yIntercept)
    {
        slope=aslope;
        anIntercept = yIntercept;
    }
    public Line (double x3)
    {
        linex = x3;
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
    else
    {
        return false;
    }
}
     public boolean equals(Line other)
     {
     if (slope==other.slope && yIntercept == other.yIntercept)
    {
        return true;
       }
    else
    {
        return false;
  }
  
}
  public boolean isParallel(Line other)
  {
      if (slope == other.slope)
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
   private double pointx;
   private double pointy;
   private double pointx1;
   private double pointy1;
   private double pointx2;
   private double pointy2;
   private double linex;
   private static final double EPSILON = 1E-12;
   private double anIntercept;

   // this method is used to check your work

 
}