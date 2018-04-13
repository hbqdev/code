/**
   A gambler will make any even probability bet if he can afford to lose.
*/
public class Gambler
{
   /**
      Constructs a gambler with a set amount of starting funds.
      @param startingFunds the amount of money he starts with.
   */
   public Gambler(double startingFunds)
   {
      funds = startingFunds;
   }
   /**
      Makes the gambler take a bet at even probability to win or lose.
      @param wager the amount of the bet
   */
   public void bet(double wager)
   {
      double random = Math.random(); // A random floating-point value between 0 and 1
      if (random < 0.5) 
         funds = funds + wager; // The gambler won
      else
         funds = funds - wager; // The gambler lost
      if (wager > funds)
       funds = funds; //gamber won't bet
    
} 
   /**
      Gets the funds remaining for the gambler.
      @return funds remaining
   */
   public double getFunds()
   {
      return funds;
   }

   private double funds;
}