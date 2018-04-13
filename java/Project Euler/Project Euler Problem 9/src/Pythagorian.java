
public class Pythagorian 
{
	private static int pro1;
	public static void main (String [] args)
	{
		for(int i=1;i<1000; i++)
		{
			for (int j = 1; j<1000;j++)
			{
				for (int k =1; k<1000;k++)
				{
					if(i*i + j*j == k*k)
					{
						if(i + j +k ==1000)
						{
							pro1 = i*j*k;
							System.out.println("num is" + pro1);
							System.out.println("nums are" + i + " " + j + " "+ k);
						}
					}
				}
			}
		}
			
	}
}
