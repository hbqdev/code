public class Faculty
{
public Faculty(String aname, String Identification)
{
name = aname;
ID = Identification;
}

public String toString()
{
return name+ID;
}


private String name;
private String ID;
private String tenured;
private boolean isTenured;
}