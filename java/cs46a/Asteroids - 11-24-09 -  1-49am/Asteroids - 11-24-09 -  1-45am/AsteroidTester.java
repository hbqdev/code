import javax.swing.JFrame;
import java.util.ArrayList;
import java.util.Random;


/**
 * Write a description of class AsteroidTester here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class AsteroidTester 
{
    public static void main(String[] args)
    {
        JFrame frame = new JFrame();
        frame.setSize(WIDTH, HEIGHT);
        frame.setTitle("AsteroidTester");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        Random r = new Random();
        
        ArrayList<Asteroid> asteroidList = new ArrayList<Asteroid>();
        ArrayList<Drawable> drawableList = new ArrayList<Drawable>();
        for (int i = 1; i <= 10; i++)
        {
            double xSpeed = 2;//r.nextDouble() * 20 - 10;
            double ySpeed = 2;//r.nextDouble() * 20 - 10;
            int size = r.nextInt(3) + 1;
            
            //asteroidList.add(new Asteroid(frame.getWidth() / 2, frame.getHeight() / 2,xSpeed,ySpeed, size, WIDTH,HEIGHT ));
        }
        
        
        
        //Creates the drawing component and adds it to the frame.
        AsteroidsComponent component = new AsteroidsComponent(drawableList);
        component.setDoubleBuffered(true);
        frame.add(component);
        frame.setVisible(true);
        
        
        boolean gameOver = false;
            while(!gameOver)
            {
                for (Asteroid asteroid : asteroidList)
                asteroid.move();
                
                Pause.pause(100);
                
                int listSize = drawableList.size();
                
                for (int k = 0; k < listSize; k++)
                    drawableList.remove(0);
                
                for (Asteroid asteroid : asteroidList)
                    drawableList.add(asteroid);
                
                component.repaint(0,0,frame.getWidth(),frame.getHeight());                
            }
    }
    
    public static final int WIDTH = 200;//1280;
    public static final int HEIGHT = 400;//768;
}
