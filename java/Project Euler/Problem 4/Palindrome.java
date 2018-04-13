
public class Palindrome 
{
	private static int num;
	public static void main (String [] args)
	{
		for(int i = 999; i>100;i--)
		{
			for(int j = 999; j>100;j--)
			{
				num = i*j;
			}
			if(num % 11 == 0)
		{
			System.out.println("The number is" + num);
		}
		}
		
	}
}
