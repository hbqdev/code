import java.util.ArrayList;
/**
   A purse holds a collection of coins.
*/
public class Purse
{
   /**
      Constructs an empty purse.
   */
   public Purse()
   {
      coins = new ArrayList<String>();
   }
   
   /**
      Adds a coin to the purse.
      @param coinName the coin to add
   */
   public void addCoin(String coinName)
   {
      coins.add(coinName);
   }
   
   /**
      Returns a string describing the object.
      @return a string in the format "Purse[coinName1,coinName2,...]"
   */
    public String toString()
   {
      coin = "Purse[";
       for (int i = 0; i<coins.size(); i++)
       {
           if (i==coins.size()-1)
             coin += coins.get(i) + "]";
             else 
             coin +=coins.get(i) + ",";
                
         }
        return coin;
    }
   
   /**
      Reverses the elements in the purse.
   */
   public void reverse()
{
     ArrayList coins2 = new ArrayList();
      for (int i = coins.size()-1; i >= 0; i--)
       {
          coins2.add(coins.get(i));
          
  }
  coins=coins2;
}

 private ArrayList<String> coins;
 private ArrayList<String>coins2;
  private String coin;
}
