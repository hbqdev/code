import java.awt.Rectangle;

public class RectangleDoubler implements Doubler
{

   public Object makeDouble(Object obj)
   {
       Rectangle a = (Rectangle) obj;       
       Rectangle newone = new Rectangle((int) a.getX(),(int) a.getY(),(int) (2*a.getWidth()), (int)(2*a.getHeight()));
       return newone;
   
    }

}

