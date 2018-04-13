import java.awt.Rectangle;
public  class FourRectanglePrinter
{
public static void main(String[]args)
{
Rectangle box = new Rectangle (5,10,50,100);
//Move Rectangle
box.translate(50,0);
System.out.println(box);
box.translate(0,100);
System.out.println(box);
box.translate(50,100);
System.out.println(box);
}
}
