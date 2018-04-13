/**
   A timer keeps tracks of the total elapsed time.
*/
public class Timer
{
   /**
      Construct a timer with 0:0O elapsed time
   */
   public Timer()
   {
      hours = 0;
      minutes = 0;
   }
   
   /**
      Adds a given number of minutes to the elapsed time.
      @param minutesToAdd the number of minutes (>=0; may be larger than 60)
   */
   public void add(int minutesToAdd)
   {
   double t = minutesToAdd;
   minutes += t;
   hours = minutes/60;
   minutes = minutes%60;
      
   }
   
   /**
      Gets the total elapsed time. 
      @return a string describing the total time in the format h:mm, 
      with mm < 60
   */
   public String getTotal()
   {
      return String.format("%d:%02d", hours, minutes);
   }
   
   private int hours;
   private int minutes;
   private int newminutes;

}