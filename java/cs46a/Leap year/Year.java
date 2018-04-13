public class Year
{
/**
 * contrucsts a class that calculates if a particular year is a leap year
 */
public Year (int someyear)
{
y=someyear;
}
public boolean isLeapYear()
{
if (y<1582)
{
if ((y%4)==0)
{
return true;
}
else
{
return false;
}
}
if (y>1528) 
{
if (((y%400)==0)  || ((y%4)==0 && (y%100) !=0))
{
return true;
}
else if ((y%400) !=0  || (y%100) == 0)
{
return false;
}
else
{
return false;
}
}
return false;
}

private int y;
}