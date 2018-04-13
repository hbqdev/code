public class PayCheck
{
public PayCheck (double wage, double hours)
{
 hourly = wage;
 worked = hours;
}
public double getPay()
{
 if (worked <=40)
 {
    paycheck =hourly*worked;
    }
    else if (worked>40)
    {
       overtime = (worked-40);
       overtimewage = hourly*1.5;
       paycheck = hourly*40 + overtimewage*overtime;
    }
    return paycheck;
}
private double paycheck;
private double hourly;
private double worked;
private double overtime;
private double overtimewage;
}
 