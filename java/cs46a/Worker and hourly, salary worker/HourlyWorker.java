
/**
 * Write a description of class HourlyWorker here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class HourlyWorker extends Worker
{
public HourlyWorker(String somename, double somesalary)
{
super(somename, somesalary);
}

public int computePay(int hours)
{
if (hours <= 40)
{
pay =  (int) (getSalary()*hours);
}
else if (hours>40)
{
int overtime = hours-40;
pay = (int) ( (getSalary()*40) + (getSalary()*1.5*overtime));
}
return pay;
 }
  private int pay;
}