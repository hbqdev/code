import java.awt.Graphics2D;
import java.awt.Image;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;

/**
 * Write a description of class Background here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Background implements Drawable
{
    public Background()
    {
        try 
          {
             image = ImageIO.read(new File("starsbg.png"));
          }
          catch (IOException ex)
          {
             System.out.println("Can't read image.");
          }
    }

    /**
     * 
     */
    public void draw(Graphics2D g2)
    {
       g2.drawImage(image, 0, 0, null);
    }
    private Image image;
}

