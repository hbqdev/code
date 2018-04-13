import java.util.*;

public class SomeCollection implemetns Iterable
{
private LinkedList data;

public collection()
{
data = new LinkedList();
}

pullic Iterator iterator()
{
Iterator<String> newiter = data.Iterator();
return newiter;
}

}