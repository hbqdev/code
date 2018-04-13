import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JComponent;
import java.util.ArrayList;
import java.util.Random;

/**
   This component draws two car shapes.
*/
public class CarComponent extends JComponent
{  

public CarComponent()
    {
        Random r =  new Random();
        cars = new ArrayList<Car>();
        houses = new ArrayList<House>();

        
        for (int i = 0; i < 5; i++)
        {
            int x = r.nextInt(300 - 60);
            int y = r.nextInt(400 - 30);
            
            int x1 = r.nextInt(300-60);
            int y1 = r.nextInt(300-30);
            cars.add(new Car(x,y));
            houses.add(new House(x1,y1,60,30));
        }
    }

   public void paintComponent(Graphics g)
   {  
      Graphics2D g2 = (Graphics2D) g;
      for (Car car : cars)
      car.draw(g2);
      
      for (House house : houses)
      house.draw(g2);
   }
   private ArrayList<Car> cars;
   private ArrayList<House>  houses;
}
