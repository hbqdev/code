public class Fibonacci {
	public static int fib(int n) 
	ArrayList
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
    for (int i=0; i<=46; i++)
        System.out.print(fib(i)+", ");
}
}
