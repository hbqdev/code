public class Dial
{
public Dial()
{
currentnumber = 0;
}

public void turnLeft()
{
currentnumber += 1;
}

public void turnRight()
{
currentnumber -=1;
if (currentnumber <0)
{
currentnumber = currentnumber +40;
}
}

public int currentNumber()
{
return currentnumber;
}
private int currentnumber;
private int temp;
private int temp1;
}