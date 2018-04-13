public class Number
/**
* Create a class that contains a method to compute the longest run of a sequence and returns its value
*/
{
/**
      Computes the length of the longest run (sequence of 
      adjacent repeated values) in an array.
      @param values an array of integer values
      @return the length of the longest run in values
   */
   public int lengthOfLongestRun(int[] values)
   {
      // int length=0;
       //int a=1;

    //for(int i=0; i<values.length;i++)
    //{
      //if ( values[i] ==values[i+1])
        //length++;
      //else if (a<length)
  //{ 
     // a+=length;
      //length=1;
        //  }
//}
 //if (a>length)
   //     return a;
     //   return length;
     if (values.length ==0)  return 0;
    int longestRunyet = 0;
    int currentRun =1;
    int previousNumber = values[0]-1;
    for (int i : values)
    {
        if (i==previousNumber)
        currentRun++;
        else
        currentRun = 1;
        if (currentRun > longestRunyet)
        longestRunyet =  currentRun;
        previousNumber = i;
    }
    // loop through the array 
    // if current number is same as previous number
    // current loop is 1 bigger than it was
    // if current is bigger than max loop so far
    // max loop = current loop
    return longestRunyet;
}
}