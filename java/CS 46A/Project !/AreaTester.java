import java.awt.Rectangle;
public  class AreaTester
{
public static void main(String[]args)
{
Rectangle box = new Rectangle (5,10,50,100);
double width=box.getWidth();
double height=box.getHeight();
System.out.println(box.getWidth()*box.getHeight());

System.out.println("Expected:5000");

}
}
