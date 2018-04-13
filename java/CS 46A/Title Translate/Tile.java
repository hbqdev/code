/*
  TODO: Override translate so that it translates by the tile's
  dimensions, not pixels. For example, translate(1, -2) should move
  by the full width to the right and twice the height up.
*/

import java.awt.Rectangle;

/**
   A tile for tiling the plane.
*/
public class Tile extends Rectangle
{
   /**
      Constructs a tile with given dimensions.
      @param x the x-coordinate of the top left corner
      @param y the y-coordinate of the top left corner
      @param width the width of the tile
      @param height the height of the tile
   */
   public Tile(int x, int y, int width, int height)
   {
      super(x, y, width, height);
   }


   // this method is used to check your work

   public static String check(int x, int y, int width, int height, int dx, int dy)
   {
      Tile t = new Tile(x, y, width, height);
      t.translate(width+width, -2*height);
      return t.toString();
   }
}
