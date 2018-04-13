/**
 * Construct  a class that keeps track of the score 
 * 
 * @author (Tin Tran) 
 */
public class ScoreKeeper
{
  
       public ScoreKeeper(int lives)
    {
        currentlives = lives;
        Score = 0;
        bonus = 1;
    }
    
    /**
     * counts the score
     * @param aScore the current score
     */
    public void addScore(int aScore)
    {
        Score +=aScore;
    }
/**
 * @return Score
 /*
 
    public int getScore()
    {
        return Score;
    }
    
      /**
     * Decrease the current lives of the ship
     */
    public void lostLife()
    {
        currentlives--;
    }
    
    /**
     * @return currentlives
     */
     public int getLives()
    {
        return currentlives;
    }
    
    /**
     * Sets bonus
     * @param aBonus bonus of the game
     */
  public void setBonus(int newBonus)
    {
        bonus = newBonus;
    }
  
 /**
  * @return bonus
  */   
 public int getBonus()
 {
     return bonus;
    }
    
   private int Score;
   private int currentlives;
   private int bonus;
}