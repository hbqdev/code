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
   private ArrayList<String> coins;
   private String coin;
}
