
/**
Construct a class to calculate the Easter day
 */
public class Easter
{

public Easter (int y)
{
someyear = y;
a  = y%19.0;
b = y/100.0;
c = y%100.0;
d = b/4.0;
e = b%4.0;
g = (8.0*b+13.0)/25.0;
h = (19.0*a+b-d-g+15.0)%30.0;
j = c/4.0;
k = c%4.0;
m = (a+11.0*h)/319.0;
r = (2.0*e+2.0*j-k-h+m+32.0)%7.0;
n = (h-m+r+90.0)/25.0;
p = (h-m+r+n+19.0)%32.0;
}


public double getEasterSundayMonth()
{
EasterSundayMonth = n;
return EasterSundayMonth;
}
public double getEasterSundayDay()
{
EasterSundayDay = p;
return EasterSundayDay;
}
private double a;
private double b;
private double c;
private double d;
private double e;
private double g;
private double h;
private double j;
private double k;
private double m;
private double r;
private double n;
private double p;

public double someyear;
public double EasterSundayMonth;
public double EasterSundayDay;
public double EasterDay;
}