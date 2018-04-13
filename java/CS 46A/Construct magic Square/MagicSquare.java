public class MagicSquare
{
public MagicSquare(int size)
{
 square = new int[size][size];
 int row = size -1;
 int col = size/2;
 for (int i =1; i <= size*size; i++)
 {
     square[row][col] = i;
     int nextRow = (row+1)%size;
     int nextCol = (col+1) %size;
     if (square[nextRow][nextCol] !=0 || (nextRow == 0 && nextCol ==0))
     {
         nextCol = col;
         nextRow = (row+size-1)%size;
           }
           row = nextRow;
           col = nextCol;
}
}
public String toString()
{
int size = square.length;
String result = "";
for (int i = 0; i<size;i++)
{
for (int j=0; j<size; j++)
result = result + String.format("%4d", square[i][j]);
result = result + String.format("%n");
}
return result;
} 

private int[][] square;
}