    import java.util.Scanner;
   
    public class DataAnalyzer
    {
       public static void main(String[] args)
      {
        Scanner in = new Scanner(System.in);
         DataSet data = new DataSet();
   
         boolean done = false;
         while (!done)
         {
            System.out.print("Enter value, Q to quit: ");
            String input = in.next();
            if (input.equalsIgnoreCase("Q"))
               done = true;
               
            else
            {
               double a = Double.parseDouble(input);
               data.add(a);
            }
         }
         System.out.println("Count = " + data.getCount());
         System.out.println("Average = " + data.getAverage());
         System.out.println("Standard Deviation = " + data.getStandardDeviation());
   
        }
   }
   
