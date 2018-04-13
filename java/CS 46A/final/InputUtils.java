import java.util.Scanner;
import java.net.URL;

public class InputUtils
{
public static void printTail (Scanner in, String firstline)
{
String line = in.nextLine();
while(in.hasNext())
{
if (line.equals(firstline))
{
System.out.println(line);
}
}
}

public static void main(String[] args) // Also in InputUtils
{
   URL url = new URL("http://horstmann.com/sjsu/cs46a/finalreview/alice30.txt");
   Scanner in = new Scanner(url.openStream());
   printTail(in, "                ALICE'S ADVENTURES IN WONDERLAND");
}
}