public class Worker
{
public Worker(String aname, double aSalary)
{
name = aname;
salary = aSalary;
}
public String getName()
{
return name;
}

public double getSalary()
{
return salary;
}

public int computePay(int hours)
{
return 0;
}
private String name;
private double salary;


}