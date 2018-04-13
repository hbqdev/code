import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JPanel;
import javax.swing.JComponent;
import java.util.ArrayList;

/**
   A component that holds all elements of 
*/
public class AsteroidsComponent extends JComponent
{  
   
    public AsteroidsComponent(ArrayList<Drawable> drawableList)
    {
        this.drawableList = drawableList;
    }

   public void paintComponent(Graphics g)
   {  
       Graphics2D g2 = (Graphics2D) g;
       
       for(Drawable drawables : drawableList)
       drawables.draw(g2);
      
   }
   
   private ArrayList<Drawable> drawableList;
}