public class Lines
{
   /**
      Computes the length of a line segment
      @param x1 the x-coordinate of the starting point
      @param y1 the y-coordinate of the starting point
      @param x2 the x-coordinate of the ending point
      @param y2 the y-coordinate of the ending point
      @return the length of the line segment joining (x1, y1) and (x2, y2)
   */
   public double segmentLength(double x1, double y1, double x2, double y2)
   {
   
   return Math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)));
   }
   private double xa;
   private double ya;
   private double xb;
   private double yb;
}