import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JComponent;
import java.awt.Color;

  /**
     This component draws two car shapes.
  */
  public class CarComponent extends JComponent
  {
   public void paintComponent(Graphics g)
   {
	 Graphics2D g2 = (Graphics2D) g;

	 Car car1 = new Car(5, 10);

	 int x = getWidth() - 60;
	 int y = getHeight() - 30;

	 Car car2 = new Car(150, 200);
     g2.setColor(Color.RED);
	 car1.draw(g2);
	 g2.setColor(Color.BLUE);
	 car2.draw(g2);
   }
 }

