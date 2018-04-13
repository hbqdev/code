
/**
 * Write a description of class Pause here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Pause
{
    public static void pause(int ms) 
    {
        //int seconds = (int)Math.floor(time);
        try
        {
            Thread.currentThread().sleep(ms); //sleep for 1000 ms
        }
        catch(InterruptedException ie)
        {
        }
    }
}
