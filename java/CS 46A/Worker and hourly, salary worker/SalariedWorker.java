
/**
 * Write a description of class SalariedWorker here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class SalariedWorker extends Worker
{
 public SalariedWorker (String aNAME, double aSALARY)
 {
     super(aNAME, aSALARY);
    }
    
    public int computePay(int hours)
    {
       int pay = (int) (getSalary()*40);
        return pay;
    }


 }