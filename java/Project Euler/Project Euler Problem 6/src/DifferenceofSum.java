
public class DifferenceofSum 
{
	private static int sum;
	private static int sum2;
	public static void main (String [] args)
	{
		for(int i = 1; i<101;i++)
		{
			sum+=i*i;
		}
		System.out.println("sum is" + " " + sum);
		for(int i =1; i<101;i++)
		{
			sum2 +=i;
		}
		System.out.println("sum 2 is" + " " + sum2);
	}
}
