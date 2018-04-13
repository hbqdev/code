import java.util.Scanner;
/**
   Computes information about a set of data values.
 */
 public class DataSet
 {
    /**
       Constructs an empty data set.
    */
    public DataSet()
   {
      sum = 0;
      count = 0;
      maximum = 0;
     }

    /**
       Adds a data value to the data set.
       @param x a data value
    */
    public void add(double x)
    {
       sum = sum + x;
       sumSquare = sumSquare +(x*x);
       if (count == 0 || maximum < x) maximum = x;
       count++;
    }

    /**
       Gets the average of the added data.
       @return the average or 0 if no data has been added
    */
   public int getCount()
   {
     return count;    
    }
    public double getAverage()
    {
       if (count == 0) return 0;
       else return sum / count;
    }

    /**
       Gets the standard deviation.
       @return the standard deviation
    */
    public double getStandardDeviation()
    {
      standarddeviation  = Math.sqrt((sumSquare - (1.0/count)*(sum)*(sum))/(count-1.0));
      return standarddeviation;
    }

    private double sum;
    private double standarddeviation;
    private double maximum;
    private int count;
    private double sumSquare;
   
 }
