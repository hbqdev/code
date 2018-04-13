public class Grade
{
/**
 * construct a class that translate letter grade into numerical grade
 */
public Grade (double agrade)
{
grade=agrade;
}
public String getLetterGrade()
{
if (grade==4)
{
return lettergrade="A+";
}
else if  (grade>=3.8 && grade<4)
{
return lettergrade="A";
}
else if (grade>=3.4 && grade<3.8)
{
return lettergrade="A-";
}
else if (grade>=3.1 && grade<3.4)
{
return lettergrade="B+";
}
else if (grade>=2.8 && grade<3.1)
{
return lettergrade="B";
}
else if (grade>=2.4 && grade<2.8)
{
return lettergrade="B-";
}
else if (grade>=2.1 && grade<2.4)
{
return lettergrade="C+";
}
else if (grade >=2 && grade <2.1)
{
return lettergrade="C";
}
else if (grade>=1.4 && grade<2)
{
return lettergrade="C-";
}
else if (grade >=1.1 && grade <1.4)
{
return lettergrade="D+";
}
else if (grade >1 && grade <=1.1)
{
return lettergrade="D";
}
else if (grade>=0.7 && grade<1)
{
return lettergrade="D-";
}
else if (grade<0.7)
{
return lettergrade="F";
}
return lettergrade;
}
private String lettergrade;
private double grade;
}