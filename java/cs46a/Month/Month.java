
/**
 construct a class month and extract each month according to each number
 */
public class Month
{
 public Month(int n)
 {
    monthnumber  = n;
    i = ((9*(n-1)) + n-1);
    j = i +9;
    String Month = "January   February  March     April     May       June      July      August    September October   November  December ";
    monthname =  Month.substring(i,j);
     }

public String getName()
{
return monthname;
}
private String monthname;
private int monthnumber;
private int i;
private int j;
}