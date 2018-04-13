/**
 a Class that will construct a square
 */
public class Square
{
/**
 Constructs a Square
 */
public Square(double side)
{
aside = side;
Area = aside*aside;
Perimeter = 4*(aside);
DiagonalLength = Math.sqrt(aside*aside+aside*aside);
}
public double getArea()
{
return Area;
}
public double getPerimeter()
{
return Perimeter;
}
public double getDiagonalLength()
{
return DiagonalLength;
}
private double aside;
private double Area;
private double Perimeter;
private double DiagonalLength;
}