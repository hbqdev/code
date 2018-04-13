public class Coin
/**
 * Construct a class which stores and computes the value of coins
 */
{
public Coin(double aValue, String aName) 
{ 
value = aValue;
coin = aName;
 }
 public String getName()
 {
     return coin;
    }
    
public double getValue()
{
return value;
 }
 private double value;
 private String coin;
 
}
