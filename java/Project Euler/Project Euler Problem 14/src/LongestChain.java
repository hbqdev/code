
public class LongestChain 
{
	private static long num;
	private static long startoflongest =0;
	private static long longestchain = 0;
	public static void main (String [] args)
	{
		for(long i=999999;i>=1;i--)
		{
			num =i;
			int count=1;
			while(num!=1)
			{
				if(num%2==0)
				num=num/2;
				else 
				num = 3*num+1;
				count++;
			}
			if(count<longestchain)
				continue;
				
			startoflongest = i;
			longestchain = count;
			
		}
		System.out.println("the longest is" + startoflongest);
	}
}
