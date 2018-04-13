public class Grade
{
/**
 * construct a class that translate letter grade into numerical grade
 */
public Grade (String agrade)
{
grade=agrade;
}
public double getNumericGrade()
{
if (grade.equals("A"))
{
return numericgrade=4;
}
else if(grade.equals("A+"))
{
return numericgrade=4;
}
else if (grade.equals("A-"))
{
return numericgrade =3.7;
}
else if (grade.equals("B"))
{
return numericgrade = 3;
}
else if (grade.equals("B+"))
{
return numericgrade = 3.3;
}
else if(grade.equals("B-"))
{
return numericgrade = 2.7;
}
else if(grade.equals("C"))
{
return numericgrade = 2;
}
else if (grade.equals("C+"))
{
return numericgrade = 2.3;
}
else if(grade.equals("C-"))
{
return numericgrade = 1.7;
}
else if (grade.equals("D"))
{
return numericgrade = 1;
}
else if(grade.equals(" D-"))
{
return numericgrade = 0.7;
}
else if(grade.equals("D+"))
{
return numericgrade = 1.3;
}
else if(grade.equals("F"))
{
return numericgrade = 0;
}
else if(grade.equals(" F-"))
{
return numericgrade = -1;
}
else if(grade.equals(" F+"))
{
return numericgrade = -1;
}
else 
{
return numericgrade = -1;
}
}
private double numericgrade;
private String grade;
}