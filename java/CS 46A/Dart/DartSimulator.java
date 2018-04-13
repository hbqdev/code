public class DartSimulator
{
public static void main (String args [])
{
Dart dart1 = new Dart();
int i;
for (i =1; i<=10;i++)
dart1.throwIntoSquare();
System.out.println("Hits: " + dart1.getHits());
System.out.println("Tries: " + dart1.getTries());

}
}