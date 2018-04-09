
#include <stdio.h>

// Echo stdin to stdout with trailing \n newlines
// I work with Zane Melcho.
int main(int argc, char**argv) {
  char c;
  int trackchar = 0;
  int i;
  c = getchar();
 
  while (c != EOF) {
     if(c=='\n')
	{
		putchar(c);
		c=getchar();
		if(c==('<'))
		{
			
			c=getchar();
			if(c==('/'))
			{
			for(i=1;i<=trackchar;i++)
		    {putchar(' ');}
			trackchar-=4;
			}						
			else
			{
			trackchar+=4;
		    for(i=1;i<=trackchar;i++)
		    {putchar(' ');}
			
			}
			putchar('<');
		}
		
		
		
		
	}
	
	putchar(c);	
	c = getchar();
}
  return 1;
}


