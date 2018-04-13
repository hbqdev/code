import java.awt.Rectangle;
public  class intersection
{
public static void main(String[]args)
{
Rectangle r1 = new Rectangle (5,10,50,100);
Rectangle r2 = new Rectangle (100,150,50,100);
Rectangle r3 = r1.intersection(r2);
System.out.println(r1);
System.out.println(r2);
System.out.println(r3);

//when the Witdh and Height of the new rectangle are negative, the two rectangles do not overlap.
}
}
