/**
   This class computes the alternating sum
   of a set of data values.
*/
public class DataSet
{
   /**
      Constructs an empty data set.
   */
   public DataSet()
   {
      final int DATA_LENGTH = 100;
      data = new double[DATA_LENGTH];
      dataSize = 0;
   }

   /**
      Adds a data value to the data set.
      @param x a data value
   */
   public void add(double x)
   {
      if (dataSize >= data.length)
      {
         // make a new array of twice the size
         double[ ] newData = new double[2 * data.length];
         // copy over all elements from data to newData
         System.arraycopy(data, 0, newData, 0, data.length);
         // abandon the old array and store in data
         // a reference to the new array
         data = newData;
   }
   data[dataSize] = x;
   dataSize++;
}

/**
   Gets the alternating sum of the added data.
   @return sum the sum of the alternating data or 0 if no data has been added
*/
public double alternatingSum()
{
for (int i =0; i<data.length; i++)
{
if (i%2==0)
sum1 += data [i]*(1);
else if (i%2!=0)
sum2 +=data [i]*(-1);
    }
    return sum1+sum2;
}
   private double[] data;
   private int dataSize;
   private int i;
   private int sum1;
   private int sum2;
  }
