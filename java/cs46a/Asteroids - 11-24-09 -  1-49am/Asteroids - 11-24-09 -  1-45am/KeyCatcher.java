import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

/**
 * Write a description of class KeyCatcher here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class KeyCatcher implements KeyListener
{
    public void keyPressed(KeyEvent e)
    {
        //System.out.println("Key = " + e.getKeyChar() + " = " + e.getKeyCode());
        
        key = e.getKeyCode();
        
        if (key == 32)
            space = true;
        else if (key == 38)
            up = true;
        else if (key == 37)
            left = true;
        else if (key == 39)
            right = true;
        else if (key == 40)
            down = true;

    }
    
    public void keyReleased(KeyEvent e)
    {
        //System.out.println("Key = " + e);
        key = e.getKeyCode();
        
        if (key == 32)
            space = false;
        else if (key == 38)
            up = false;
        else if (key == 37)
            left = false;
        else if (key == 39)
            right = false;
        else if (key == 40)
            down = false;
        key = 0;
    }
    
    public void keyTyped(KeyEvent e)
    {
        //System.out.println("Key = " + e);
    }
    
    public static int getKey()
    {
        return key;
    }
    
    public static boolean spacePressed()
    {
        return space;    
    }
    
    public static boolean upPressed()
    {
        return up;
    }
    
    public static boolean leftPressed()
    {
        return left;
    }
    
    public static boolean rightPressed()
    {
        return right;
    }
    
    public static boolean downPressed()
    {
        return down;
    }
    
    
    private static int key;
    private static boolean space;
    private static boolean up;
    private static boolean left;
    private static boolean right;
    private static boolean down;

}
