import java.awt.*;
import javax.swing.*;
import java.awt.Color;

public class Pattern1 extends JComponent
{
   public static final int GRID_SIZE = 20;
   public static final int ROWS = 10;
   public static final int COLUMNS = 10;

   /**
      Draws a rectangle at the given row and column position
      @param row the row number between 0 (inclusive) and 10 (exclusive)
      @oaram column the column number between 0 (inclusive) and 10 (exclusive)
      @param color the color (such as Color.RED or Color.BLUE)
   */
   public void drawRectangle(int row, int column, Color color) 
   {
      g2.setColor(color);
      g2.fill(new Rectangle(column * GRID_SIZE, row * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1));
   }

   public void paintComponent(Graphics g)
   {
      g2 = (Graphics2D) g;
     g2.setColor(Color.RED);
     for (int i=0; (i<=3 || i>=8) && (i<=10);i++)
     {
      for (int j =0;j<=10;j++);
     {
         g2.drawRectangle(i,j,Color.RED);
        }
    }
    for (int k=4; k<=7;k++)
    {
        for (int i =0;i<=10;i++);
     {
         g2.drawRectangle(i,j,Color.RED);
        }
        
    }
      

      // Write one or more loops calling the drawRectangle method 
      // to produce the desired pattern
     
   
     


   }

   // You don't need to look at the code below

   public Dimension getPreferredSize() 
   {
      return new Dimension(GRID_SIZE * COLUMNS,
         GRID_SIZE * ROWS);
   }
   
   public static void main(String[] args)
   {
      JFrame frame = new JFrame();
      frame.add(new Pattern1());
      frame.pack();
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
   }

   private Graphics2D g2; 
}