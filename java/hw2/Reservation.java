/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package programmingassignment1;
import java.util.Scanner;
import java.util.GregorianCalendar;
import java.util.Calendar;
import java.io.FileReader;
import java.io.IOException;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.BufferedWriter;
/**
 *Create a request from an input file and add it to the room
 *Create a request from the input of a console, then execute "add" , "Cancel", "Display", "Quit"
 * @author Tin Tran
 */
public class Reservation
{
   public static void main (String argsp[]) throws IOException
    {
        Room room1 = new Room (50);
        Room room2 = new Room (200);
        MonthlySchedule schedule1 = new MonthlySchedule();
       String months[] = {
	"Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec" };
	int year ;
        // get today's date
	GregorianCalendar gcalendar = new GregorianCalendar() ; 
        System.out.println("Welcome to the Reservation program! Today is" + " " + months[gcalendar.get(Calendar.MONTH)] + " " + gcalendar.get(Calendar.DATE) + " " + gcalendar.get(Calendar.YEAR));
	     
        System.out.println("Enter the file name that contains the existing schedule.txt");
        Scanner sr1 = new Scanner (System.in);
        String file1 = sr1.next();
        Scanner sr2 = new Scanner (new FileReader(file1));

        while(sr1.hasNextLine())
        {
            String line1 = sr1.nextLine();
            String[] linea = line1.split(";");

            int monthNum = monthConv(linea[3]);
            Calendar gcal1 = new GregorianCalendar(2009,monthNum,Integer.parseInt(linea[4]), Integer.parseInt(linea[5]), 0);

            Request request1 = new Request(linea[0],linea[1], gcal1, Integer.parseInt(linea[6]),Integer.parseInt(linea[7]));

                    if(request1.getDate().get(Calendar.HOUR_OF_DAY)>=9 && (request1.getDate().get(Calendar.HOUR_OF_DAY)+ request1.getDuration())<=22);
                        {
                           if(request1.getSeats()>= room1.getCapacity())
                           {
                               if(request1.getSeats()>room2.getCapacity())
                               {
                                  System.out.println("Error, request exceeds room Capacity. Request cannot be made, program will now schedule next request");
                               }
                               else if (request1.getSeats()<=room2.getCapacity() && request1.getSeats()>room1.getCapacity())
                               {
                                  room2.add(request1);
                               }
                           }
                                else if(request1.getSeats()<=room1.getCapacity())
                               {
                                  room1.add(request1);
                               }
                   else
                       System.out.println("Error, request is not within business hour");
                         }


        }

                     
    String input = "";
      while (!input.equals("quit"))
      {
         System.out.println("type 'add' to add, 'cancel' to cancel,"
               + "or 'quit' to quit");
         input = sr1.nextLine();
         if (input.equals("add"))
         {
            System.out.println("Input Request string");
            String string1 = sr1.nextLine();
            String[] requestarray = string1.split(";");

            int monthNum2 = Request.monthConv(requestarray[3]);

            Calendar gcal2 = new GregorianCalendar(2009,monthNum2,
                  Integer.parseInt(requestarray[4]), Integer.parseInt(requestarray[5]), 0);
            Request request2 = new Request(requestarray[0], requestarray[1], gcal2,
                  Integer.parseInt(requestarray[6]), Integer.parseInt(requestarray[7]));

            if(request2.getDate().get(Calendar.HOUR_OF_DAY)>=9 && (request2.getDate().get(Calendar.HOUR_OF_DAY)+ request2.getDuration())<=22);
                        {
                           if(request2.getSeats()>= room1.getCapacity())
                           {
                               if(request2.getSeats()>room2.getCapacity())
                               {
                                  System.out.println("Error, request exceeds room Capacity. Request cannot be made, program will now schedule next request");
                               }
                               else if (request2.getSeats()<=room2.getCapacity() && request2.getSeats()>room1.getCapacity())
                               {
                                  room2.add(request2);
                               }
                           }
                                else if(request2.getSeats()<=room1.getCapacity())
                               {
                                  room1.add(request2);
                               }
                   else
                       System.out.println("Error, request is not within business hour");
                         }


            if(room1.add(request2))
                System.out.println("added: " + room1.add(request2));
            if(room2.add(request2))
                System.out.println("added: " + room2.add(request2));
         }


         else if (input.equals("cancel"))
         {
            System.out.println("Input name : ");
            String name = sr1.next();
            System.out.println("Input month : ");
            int month = monthConv(sr1.next());
            
            if(name.equals(room1.getRequest(month, name).getName()))
            System.out.println("cancelled: " + room1.cancel(room1.getRequest(month, name)));

            else if(name.equals(room2.getRequest(month, name).getName()))
            System.out.println("cancelled: " + room2.cancel(room2.getRequest(month, name)));
         }

         else if (input.equals("display"))
         {
             System.out.println("Input month : ");
             int month = sr1.nextInt();
             System.out.println(room1.printMonthly(month));
             System.out.println(room2.printMonthly(month));
         }


         else if (input.equals("quit"))
            for (int m = 0; m < 12-1; m++)
            {
               PrintWriter fOut = new PrintWriter(new BufferedWriter(new FileWriter(output.txt)));
               fOut.println(room1.printMonthly(m));
               fOut.println(room2.printMonthly(m));
            }
            System.exit(0);
      }
   }



   public static int monthConv(String monthName)
   {
      if (monthName.equalsIgnoreCase("January"))
         return 0;
      else if (monthName.equalsIgnoreCase("February"))
         return 1;
      else if (monthName.equalsIgnoreCase("March"))
         return 2;
      else if (monthName.equalsIgnoreCase("April"))
         return 3;
      else if (monthName.equalsIgnoreCase("May"))
         return 4;
      else if (monthName.equalsIgnoreCase("June"))
         return 5;
      else if (monthName.equalsIgnoreCase("July"))
         return 6;
      else if (monthName.equalsIgnoreCase("August"))
         return 7;
      else if (monthName.equalsIgnoreCase("September"))
         return 8;
      else if (monthName.equalsIgnoreCase("October"))
         return 9;
      else if (monthName.equalsIgnoreCase("November"))
         return 10;
      else if (monthName.equalsIgnoreCase("December"))
         return 11;

      return -1;
   }
}


        


    

