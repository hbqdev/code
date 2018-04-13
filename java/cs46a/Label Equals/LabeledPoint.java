// TODO: Implement equals

public class LabeledPoint
{
   /**
      Constructs a labeled point with a given position and label.
      @param anX the x-coordinate of the point
      @param aY the y-coordinate of the point
      @param aLabel the label of the point
   */
   public LabeledPoint(double anX, double aY, String aLabel)
   {
      x = anX;
      y = aY;
      label = aLabel;
   }

 public boolean equals(double aX, double bY, String bLabel)
 {
       return x == aX && y==bY && label.equals(bLabel);
    }

   public static boolean check(double x1, double y1, String s1, double x2, double y2, String s2)
   {
      LabeledPoint lp1 = new LabeledPoint(x1, y1, s1);
      LabeledPoint lp2 = new LabeledPoint(x2, y2, s2);
      return lp1.equals(lp2);
   }

   private double x;
   private double y;
   private String label;
}
