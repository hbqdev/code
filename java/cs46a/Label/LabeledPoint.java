// TODO: implement toString

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

   public String toString()
   {
       return "LabeledPoint[x="+x+",y="+y+",label=Hello]";

    }

   public static String check(double x, double y, String s)
   {
      LabeledPoint lp = new LabeledPoint(x, y, s);
      return lp.toString();
   }

   private double x;
   private double y;
   private String label;
}
