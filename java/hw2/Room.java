/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package programmingassignment1;
import java.util.Calendar;

/**
 *Room class construc a room with a list of request in 12 months
 * @author Tin Tran
 */
public class Room
{
private int capacity;
private MonthlySchedule[] roommonthlySchedule;

/**
 *Construc a room with some capcity and initialize an array of MonthlySChedule objects
 * @param Capacity capacity of the room
 */
public Room (int Capacity)
{
   capacity = Capacity;
   roommonthlySchedule = new MonthlySchedule[12];
   for (int i = 0; i<roommonthlySchedule.length;i++)
   {
       roommonthlySchedule[i] = new MonthlySchedule();
   }
}
/**
 * Add a request to the MonthlySchedule list of the room according the the month requested
 * @param request the request that will be added if there's no conflict
 * @return true if add is successful
 * @Precondition : request is not added
 * @Poscondition : request is checked and added
 */
public boolean add(Request request)
{
    int monthnum = request.getDate().get(Calendar.MONTH);
    roommonthlySchedule[monthnum].add(request);
    return true;
}

/**
 * Cancel a request that has the name requested
 * @param request the request to be cancel
 * @return true if cancel is sucessful
 * @Precondition : request is not canceled
 * @Postconidition: request is canceled
 */
public boolean cancel(Request request)
{
    
    String name = request.getName();
    int month = request.getDate().get(Calendar.MONTH);
    roommonthlySchedule[month].cancel(name);
    return true;
}
 
/**
 * Get the capacity of the room
 * @return capacity of the room
 * @Postcondidtion : capacity of the room is returned
 */
public int getCapacity()
{
 return capacity;   
}

/**
 * Get a request with the specific name
 * @param month the month in which the request is scheduled
 * @param name name of the person of the request
 * @return the request the has the name
 * Precondition : request is not found
 * Postcondition :request if found and returned
 */
public Request getRequest(int month, String name)
{
    return roommonthlySchedule[0].getrequest(name);
}

/**
 * Print out all the requests a paritcular month
 * @param m the month that needs to be printed out
 * @return a string contains all the requests of month m
 * @Precondition : requests are not printed
 * @Postcondition : all the requests of month m is printed
 */
public String printMonthly(int m)
{
    return "" + roommonthlySchedule[m];
}
}
