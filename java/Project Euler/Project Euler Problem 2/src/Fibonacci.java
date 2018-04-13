import java.util.*;
public class Fibonacci {
	public static int fib(int n) 
	
	{
    if (n < 2) {
      return n;
                }
                else {
		   return fib(n-1)+fib(n-2);
                }
	}
	public static void main(String[] args) 
{
	int sum = 0;
    for (int i=0; i<=40; i++)
    {
    	//System.out.print(fib(i)+",");
    	if(fib(i)<4000000)
    	{
    		if(fib(i)%2 ==0)
    		{
    			sum +=fib(i);
    		}
    	//num.add(fib(i));
    	}        
    }
    
   System.out.println("sum is " + sum);
    //System.out.println("sum is:" + sum);
}
}
