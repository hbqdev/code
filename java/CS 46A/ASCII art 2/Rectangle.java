/**
   A rectangle that is printed using "ASCII art".
*/
public class Rectangle
{
   /**
      Constructs a rectangle with a given width and height.
      @param aWidth the width (including the corners)
      @param aHeight the height (including the corners)
   */
   public Rectangle(int aWidth, int aHeight)
   {
      width = aWidth;
      height = aHeight;
   }

   /**
      Gets the width of this rectangle.
      @return the width
   */
   public int getWidth()
   {
      return width;
   }

   /**
      Gets the height of this rectangle.
      @return the height
   */
   public int getHeight()
   {
      return height;
   }

   /**
      Prints the rectangle.
   */
   public void print()
   {
      for (int i = 1; i <= height; i++)
      {
         printLine(i);         
      }
   }

   /**
      Prints one line of the rectangle.
      @param i the line to print (1 <= i <= height)
   */
   public void printLine(int i)
   {
      if (i == 1 || i == height)
         printHelper('+', '-');
      else
         printHelper('|', ' ');
   }

   /**
      Prints one line of the rectangle.
      @param boundary the character to be used at the left and
      right boundary
      @param middle the character to be used elsewhere
   */
   public void printHelper(char boundary, char middle)
   {
      System.out.print(boundary);
      for (int j = 2; j < width; j++)
         System.out.print(middle);
      System.out.println(boundary);
   }

   private int width;
   private int height;
}

