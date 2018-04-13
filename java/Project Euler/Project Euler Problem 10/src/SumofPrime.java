
public class SumofPrime 
{
	private static int sum;
	public static void main (String [] args)
	{
		for(int i=2;i<2000000;i++)
		{
			for(int j=2;j<2000000;j++)
			{
				if(i%j !=0)
				{
					sum+=i;
					
				}
			}
		}
		System.out.println("sum is" + sum);
	}
}
