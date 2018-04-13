public class SquareBoard
{
   /**
      Constructs an empty square game board.
      @param sideLength the length of each side
   */
   public SquareBoard(int sideLength)
   {
      length = sideLength;
      board = new String[length][length];
      // Fill with spaces
      for (int i = 0; i < length; i++)
         for (int j = 0; j < length; j++)
            board[i][j] = " ";
   }

   /**
      Creates a string representation of the board, such as
      |x o|
      | x |
      | o |.
      @return the string representation
   */
   public String toString()
   {
      String r = "";
      for (int i = 0; i < length; i++)
      {
         r = r + "|";
         for (int j = 0; j < length; j++)
            r = r + board[i][j];
         r = r + "|\n";
      }
      return r;
   }   

   /**
      Fills the borders of this board with "*" strings.
   */
   public void fillBorders()
   {
      // your work here
      for (int i = 0; i<board.length;i++)
      {
          board [i][0] = "*";
          board[length-1][i] = "*";
          board[0][i] = "*";
          board[i][length-1] = "*";
        }


   }

   private String[][] board;
   private int length;


   public static void main(String[] args)
   {
      SquareBoard chessBoard = new SquareBoard(8);
      chessBoard.fillBorders();
      System.out.println(chessBoard.toString());
   }
}
